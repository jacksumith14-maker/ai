
import os

from ai_modules.resume_parser import extract_resume_text
from ai_modules.skill_extractor import extract_skills
from ai_modules.resume_scorer import calculate_resume_score
from ai_modules.analysis_database import save_analysis_result

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

        score, breakdown = calculate_resume_score(
            resume_text, skills
        )

        # Resume ID 1 is used for this initial test
        success = save_analysis_result(
            1, score, breakdown
        )

        if success:
            print("ANALYSIS SAVED SUCCESSFULLY!")
            print("Resume Score:", score, "/ 100")
        else:
            print("Could not save analysis.")

    else:
        print("Could not extract resume text.")

else:
    print("No PDF resume found.")
