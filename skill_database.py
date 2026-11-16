
from config import get_db_connection


def save_resume_skills(resume_id, extracted_skills):

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        for skill in extracted_skills:

            # Add skill if it does not already exist
            cursor.execute(
                """
                INSERT INTO skills (skill_name)
                VALUES (%s)
                ON DUPLICATE KEY UPDATE skill_name = VALUES(skill_name)
                """,
                (skill,)
            )

            # Get skill ID
            cursor.execute(
                "SELECT skill_id FROM skills WHERE skill_name = %s",
                (skill,)
            )

            skill_result = cursor.fetchone()
            skill_id = skill_result[0]

            # Connect skill with resume
            cursor.execute(
                """
                INSERT IGNORE INTO resume_skills
                (resume_id, skill_id)
                VALUES (%s, %s)
                """,
                (resume_id, skill_id)
            )

        connection.commit()
        return True

    except Exception as error:
        if connection:
            connection.rollback()

        print("SKILL DATABASE ERROR:", repr(error))
        return False

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
