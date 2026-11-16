
from ai_modules.text_matcher import calculate_text_similarity

resume_text = """
I have knowledge of HTML, CSS, JavaScript, React,
MySQL and Git. I have developed responsive websites
and web applications.
"""

job_description = """
Frontend Developer required to build responsive websites
using HTML, CSS, JavaScript, React and Git.
"""

score = calculate_text_similarity(
    resume_text,
    job_description
)

print("===== TF-IDF SIMILARITY TEST =====")
print("Resume and Job Similarity:", score, "%")
print("TEST COMPLETED SUCCESSFULLY")
