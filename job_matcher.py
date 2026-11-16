
import os
import pymupdf

from config import get_db_connection
from ai_modules.text_matcher import calculate_text_similarity


def calculate_job_matches(resume_id):

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Get original resume PDF filename
        cursor.execute("""
            SELECT stored_filename
            FROM resumes
            WHERE resume_id = %s
        """, (resume_id,))

        resume_file = cursor.fetchone()

        if not resume_file:
            return []

        # Extract text from uploaded PDF
        resume_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "uploads",
            resume_file["stored_filename"]
        )

        document = pymupdf.open(resume_path)
        resume_text = ""

        try:
            for page in document:
                resume_text += page.get_text() + "\n"
        finally:
            document.close()

        # Get skills from the selected resume
        cursor.execute("""
            SELECT s.skill_name
            FROM resume_skills rs
            JOIN skills s ON rs.skill_id = s.skill_id
            WHERE rs.resume_id = %s
        """, (resume_id,))

        resume_skills = {
            row["skill_name"].lower()
            for row in cursor.fetchall()
        }

        # Get all available jobs
        cursor.execute("""
            SELECT job_id, job_title, company_name,
                   job_description, location, experience_required
            FROM jobs
        """)

        jobs = cursor.fetchall()
        results = []

        # Compare resume with every job
        for job in jobs:

            cursor.execute("""
                SELECT s.skill_name
                FROM job_skills js
                JOIN skills s ON js.skill_id = s.skill_id
                WHERE js.job_id = %s
            """, (job["job_id"],))

            required_skills = {
                row["skill_name"].lower()
                for row in cursor.fetchall()
            }

            # Calculate skill match
            matched_skills = resume_skills.intersection(
                required_skills
            )

            if required_skills:
                skill_match = round(
                    len(matched_skills) /
                    len(required_skills) * 100
                )
            else:
                skill_match = 0

            # Calculate TF-IDF text similarity
            text_similarity = calculate_text_similarity(
                resume_text,
                job["job_description"] or ""
            )

            # Calculate combined match percentage
            final_match = round(
                (skill_match * 0.7) +
                (text_similarity * 0.3)
            )

            results.append({
                "job_title": job["job_title"],
                "company_name": job["company_name"],
                "location": job["location"],
                "experience": job["experience_required"],
                "skill_match": skill_match,
                "text_similarity": text_similarity,
                "match_percentage": final_match,
                "matched_skills": sorted(matched_skills),
                "missing_skills": sorted(
                    required_skills - resume_skills
                )
            })

        # Sort jobs by final match percentage
        results.sort(
            key=lambda item: item["match_percentage"],
            reverse=True
        )

        return results

    except Exception as error:
        print("JOB MATCHING ERROR:", repr(error))
        return []

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
