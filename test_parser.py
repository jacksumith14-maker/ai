
import os
from ai_modules.resume_parser import extract_resume_text

resume_folder = "uploads"

files = [
    file for file in os.listdir(resume_folder)
    if file.lower().endswith(".pdf")
]

if files:
    file_path = os.path.join(resume_folder, files[0])

    text = extract_resume_text(file_path)

    if text:
        print("RESUME TEXT EXTRACTED SUCCESSFULLY!")
        print("--------------------------------")
        print(text)
    else:
        print("No extractable text found in this PDF.")
else:
    print("No PDF resume found in uploads folder.")
