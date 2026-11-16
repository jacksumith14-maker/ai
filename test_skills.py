
import os

from ai_modules.resume_parser import extract_resume_text
from ai_modules.skill_extractor import extract_skills

resume_folder = "uploads"

files = [
    file for file in os.listdir(resume_folder)
    if file.lower().endswith(".pdf")
]

if files:

    file_path = os.path.join(resume_folder, files[0])

    resume_text = extract_resume_text(file_path)

    if resume_text:

        skills = extract_skills(resume_text)

        print("SKILL EXTRACTION SUCCESSFUL!")
        print("----------------------------")
        print("Skills Found:")

        if skills:
            for skill in skills:
                print("-", skill)
        else:
            print("No matching skills found.")

    else:
        print("Could not extract resume text.")

else:
    print("No PDF resume found.")
