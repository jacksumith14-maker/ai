
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import get_db_connection

from ai_modules.resume_parser import extract_resume_text
from ai_modules.skill_extractor import extract_skills
from ai_modules.skill_database import save_resume_skills
from ai_modules.career_recommender import recommend_careers
from ai_modules.job_matcher import calculate_job_matches

import mysql.connector
import os
import uuid
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Flask application
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path, "uploads"
)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

app.secret_key = os.getenv("SECRET_KEY", "development-key")


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# DATABASE CONNECTION TEST
@app.route("/db-test")
def db_test():

    try:
        connection = get_db_connection()
        connection.close()

        return "SUCCESS! Flask connected to MySQL Database."

    except Exception as error:
        print("DATABASE ERROR:", repr(error))
        return f"Database Connection Failed: {error}"


# USER REGISTRATION
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not full_name or not email or not password:
            flash("Please fill in all required fields.")

        elif password != confirm_password:
            flash("Passwords do not match.")

        elif len(password) < 8:
            flash("Password must contain at least 8 characters.")

        else:

            connection = None
            cursor = None

            try:
                connection = get_db_connection()
                cursor = connection.cursor()

                hashed_password = generate_password_hash(password)

                query = """
                    INSERT INTO users
                    (full_name, email, password_hash)
                    VALUES (%s, %s, %s)
                """

                cursor.execute(
                    query,
                    (full_name, email, hashed_password)
                )

                connection.commit()

                flash("Registration successful! You can now log in.")

            except mysql.connector.IntegrityError:
                flash("This email is already registered.")

            except Exception as error:
                print("REGISTRATION ERROR:", repr(error))
                flash("Something went wrong. Please try again.")

            finally:
                if cursor:
                    cursor.close()

                if connection and connection.is_connected():
                    connection.close()

    return render_template("register.html")


# USER LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            query = """
                SELECT user_id, full_name, email, password_hash
                FROM users
                WHERE email = %s
            """

            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[3], password):

                session["user_id"] = user[0]
                session["user_name"] = user[1]

                return redirect(url_for("dashboard"))

            flash("Invalid email or password.")

        except Exception as error:
            print("LOGIN ERROR:", repr(error))
            flash("Something went wrong. Please try again.")

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    return render_template("login.html")


# USER DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session["user_name"]
    )


# USER LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# RESUME UPLOAD AND SKILL EXTRACTION
@app.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        file = request.files.get("resume")

        if not file or file.filename == "":
            flash("Please select a resume.")

        elif not file.filename.lower().endswith(".pdf"):
            flash("Only PDF files are allowed.")

        else:

            original_filename = secure_filename(file.filename)
            stored_filename = uuid.uuid4().hex + ".pdf"

            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                stored_filename
            )

            connection = None
            cursor = None
            resume_saved = False

            try:

                # 1. Save uploaded PDF
                file.save(file_path)

                # 2. Extract text from PDF
                resume_text = extract_resume_text(file_path)

                if not resume_text or not resume_text.strip():
                    raise ValueError(
                        "No readable text found in the PDF."
                    )

                print(
                    "EXTRACTED TEXT LENGTH:",
                    len(resume_text)
                )

                # 3. Extract skills
                extracted_skills = extract_skills(resume_text)

                print(
                    "EXTRACTED SKILLS:",
                    extracted_skills
                )

                # 4. Save resume details in MySQL
                connection = get_db_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO resumes
                    (user_id, original_filename, stored_filename)
                    VALUES (%s, %s, %s)
                """, (
                    session["user_id"],
                    original_filename,
                    stored_filename
                ))

                # Get newly created resume ID
                resume_id = cursor.lastrowid

                connection.commit()
                resume_saved = True

                # 5. Save extracted skills
                if extracted_skills:

                    skills_saved = save_resume_skills(
                        resume_id,
                        extracted_skills
                    )

                    if skills_saved:
                        flash(
                            "Resume uploaded successfully! "
                            "Skills extracted and saved."
                        )
                    else:
                        flash(
                            "Resume uploaded, but skill saving failed. "
                            "Check the terminal."
                        )

                else:
                    flash(
                        "Resume uploaded, but no supported skills "
                        "were found."
                    )

            except Exception as error:

                print(
                    "RESUME UPLOAD ERROR:",
                    repr(error)
                )

                if connection and connection.is_connected():
                    connection.rollback()

                # Remove the file only if its database record
                # was not successfully saved.
                if not resume_saved and os.path.exists(file_path):
                    os.remove(file_path)

                flash(
                    "Resume upload failed. "
                    "Check terminal for details."
                )

            finally:

                if cursor:
                    cursor.close()

                if connection and connection.is_connected():
                    connection.close()

    return render_template("upload_resume.html")


# RESUME ANALYSIS REPORT
@app.route("/analysis")
def analysis():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None
    result = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                ar.total_score,
                ar.skill_score,
                ar.education_score,
                ar.project_score,
                ar.experience_score,
                ar.completeness_score,
                ar.analyzed_at
            FROM analysis_results ar
            JOIN resumes r
                ON ar.resume_id = r.resume_id
            WHERE r.user_id = %s
            ORDER BY ar.analyzed_at DESC
            LIMIT 1
        """

        cursor.execute(query, (session["user_id"],))
        result = cursor.fetchone()

    except Exception as error:

        print("ANALYSIS PAGE ERROR:", repr(error))
        flash("Unable to load analysis report.")

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

    return render_template(
        "analysis.html",
        result=result,
        name=session["user_name"]
    )


# JOB RECOMMENDATIONS
@app.route("/recommendations")
def recommendations():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT resume_id
            FROM resumes
            WHERE user_id = %s
            ORDER BY upload_date DESC
            LIMIT 1
        """, (session["user_id"],))

        resume = cursor.fetchone()

        if not resume:
            flash("Please upload your resume first.")
            return redirect(url_for("upload_resume"))

        resume_id = resume[0]

        # Generate job recommendations
        job_results = calculate_job_matches(resume_id)

        return render_template(
            "recommendations.html",
            jobs=job_results
        )

    except Exception as error:

        print("RECOMMENDATION PAGE ERROR:", repr(error))
        flash("Unable to load job recommendations.")

        return redirect(url_for("dashboard"))

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# CAREER RECOMMENDATIONS
@app.route("/career-recommendations")
def career_recommendations():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Get latest resume of logged-in user
        cursor.execute("""
            SELECT resume_id
            FROM resumes
            WHERE user_id = %s
            ORDER BY upload_date DESC
            LIMIT 1
        """, (session["user_id"],))

        resume = cursor.fetchone()

        if not resume:
            flash("Please upload your resume first.")
            return redirect(url_for("upload_resume"))

        resume_id = resume[0]

        # Retrieve skills from MySQL
        cursor.execute("""
            SELECT s.skill_name
            FROM resume_skills rs
            JOIN skills s
                ON rs.skill_id = s.skill_id
            WHERE rs.resume_id = %s
        """, (resume_id,))

        rows = cursor.fetchall()

        resume_skills = [row[0] for row in rows]

        print("CAREER RESUME SKILLS:", resume_skills)

        # Generate career recommendations
        career_results = recommend_careers(resume_skills)

        return render_template(
            "career_recommendations.html",
            careers=career_results
        )

    except Exception as error:

        print("CAREER RECOMMENDATION PAGE ERROR:", repr(error))
        flash("Unable to load career recommendations.")

        return redirect(url_for("dashboard"))

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# RUN FLASK APPLICATION
if __name__ == "__main__":
    app.run(debug=True)
