
def calculate_resume_score(resume_text, extracted_skills):

    score = 0
    breakdown = {}

    # 1. Technical Skills - 40 marks
    skill_score = min(len(extracted_skills) * 5, 40)
    breakdown["Technical Skills"] = skill_score

    # 2. Education - 20 marks
    education_keywords = [
        "education", "degree", "bachelor",
        "master", "b.e", "b.tech", "b.sc",
        "college", "university"
    ]

    education_count = sum(
        1 for word in education_keywords
        if word in resume_text.lower()
    )

    education_score = min(education_count * 3, 20)
    breakdown["Education"] = education_score

    # 3. Projects - 20 marks
    project_keywords = [
        "project", "developed", "implementation",
        "application", "system"
    ]

    project_count = sum(
        1 for word in project_keywords
        if word in resume_text.lower()
    )

    project_score = min(project_count * 4, 20)
    breakdown["Projects"] = project_score

    # 4. Experience - 10 marks
    experience_keywords = [
        "experience", "internship",
        "intern", "work experience"
    ]

    experience_count = sum(
        1 for word in experience_keywords
        if word in resume_text.lower()
    )

    experience_score = min(experience_count * 5, 10)
    breakdown["Experience"] = experience_score

    # 5. Resume Completeness - 10 marks
    completeness_keywords = [
        "email", "phone", "skills",
        "education", "project"
    ]

    completeness_count = sum(
        1 for word in completeness_keywords
        if word in resume_text.lower()
    )

    completeness_score = completeness_count * 2
    breakdown["Completeness"] = completeness_score

    score = sum(breakdown.values())

    return score, breakdown
