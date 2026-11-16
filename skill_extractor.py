
import re

SKILL_DICTIONARY = {
    "Python": ["python"],
    "Java": ["java"],
    "C": ["c"],
    "C++": ["c++"],
    "HTML": ["html"],
    "CSS": ["css"],
    "JavaScript": ["javascript", "js"],
    "React": ["react", "reactjs"],
    "Flask": ["flask"],
    "Django": ["django"],
    "MySQL": ["mysql"],
    "SQL": ["sql"],
    "MongoDB": ["mongodb"],
    "Machine Learning": ["machine learning"],
    "Artificial Intelligence": ["artificial intelligence", "ai"],
    "Data Science": ["data science"],
    "Git": ["git"],
    "Bootstrap": ["bootstrap"],
    "PHP": ["php"],
    "Node.js": ["node.js", "nodejs"]
}


def extract_skills(resume_text):

    found_skills = []

    text = resume_text.lower()

    for skill, keywords in SKILL_DICTIONARY.items():

        for keyword in keywords:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(keyword)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills
