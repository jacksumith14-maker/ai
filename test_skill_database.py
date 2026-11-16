
import os

from ai_modules.resume_parser import extract_resume_text
from ai_modules.skill_extractor import extract_skills
from ai_modules.skill_database import save_resume_skills

resume_folder = "uploads"

files = [
    file for file in os.listdir(resume_folder)
    if file.lower().endswith(".pdf")
]

if files:

    resume_file = files[0]
    file_path = os.path.join(resume_folder, resume_file)

    resume_text = extract_resume_text(file_path)

    if resume_text:

        extracted_skills = extract_skills(resume_text)

        # Use resume ID 1 for this initial test
        success = save_resume_skills(1, extracted_skills)

        if success:
            print("SKILLS SAVED SUCCESSFULLY!")
            print("Skills:", extracted_skills)
        else:
            print("Failed to save skills.")

    else:
        print("Could not extract resume text.")

else:
    print("No PDF found.")
