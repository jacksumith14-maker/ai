
from config import get_db_connection
from ai_modules.career_recommender import recommend_careers

connection = None
cursor = None

try:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get the latest uploaded resume
    cursor.execute("""
        SELECT resume_id
        FROM resumes
        ORDER BY upload_date DESC
        LIMIT 1
    """)

    resume = cursor.fetchone()

    if not resume:
        print("No uploaded resume found.")

    else:
        resume_id = resume["resume_id"]

        # Get skills stored in MySQL
        cursor.execute("""
            SELECT s.skill_name
            FROM resume_skills rs
            JOIN skills s
            ON rs.skill_id = s.skill_id
            WHERE rs.resume_id = %s
        """, (resume_id,))

        rows = cursor.fetchall()

        resume_skills = [
            row["skill_name"]
            for row in rows
        ]

        print("\n===== MYSQL CAREER RECOMMENDATION TEST =====")

        print("Resume ID:", resume_id)
        print("Resume Skills:", resume_skills)

        # Generate career recommendations
        results = recommend_careers(resume_skills)

        for result in results:

            print("\n------------------------------")

            print("Career:", result["career"])

            print("Match:", result["match_percentage"], "%")

            print("Matched Skills:", result["matched_skills"])

            print("Missing Skills:", result["missing_skills"])

        print("\nMYSQL CAREER RECOMMENDATION TEST COMPLETED!")

except Exception as error:
    print("CAREER DATABASE ERROR:", repr(error))

finally:
    if cursor:
        cursor.close()

    if connection and connection.is_connected():
        connection.close()
