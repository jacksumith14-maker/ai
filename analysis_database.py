
from config import get_db_connection


def save_analysis_result(resume_id, score, breakdown):

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO analysis_results (
                resume_id,
                total_score,
                skill_score,
                education_score,
                project_score,
                experience_score,
                completeness_score
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)

            ON DUPLICATE KEY UPDATE
                total_score = VALUES(total_score),
                skill_score = VALUES(skill_score),
                education_score = VALUES(education_score),
                project_score = VALUES(project_score),
                experience_score = VALUES(experience_score),
                completeness_score = VALUES(completeness_score),
                analyzed_at = CURRENT_TIMESTAMP
        """

        values = (
            resume_id,
            score,
            breakdown["Technical Skills"],
            breakdown["Education"],
            breakdown["Projects"],
            breakdown["Experience"],
            breakdown["Completeness"]
        )

        cursor.execute(query, values)
        connection.commit()

        return True

    except Exception as error:
        if connection:
            connection.rollback()

        print("ANALYSIS DATABASE ERROR:", repr(error))
        return False

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
