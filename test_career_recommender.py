
from ai_modules.career_recommender import recommend_careers

print("\n===== CAREER RECOMMENDATION TEST =====")

# Sample resume skills
resume_skills = [
    "Java",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "MySQL",
    "SQL",
    "Git"
]

# Generate career recommendations
results = recommend_careers(resume_skills)

# Display results
for result in results:

    print("\n------------------------------")
    print("Career:", result["career"])
    print("Match:", result["match_percentage"], "%")
    print("Matched Skills:", result["matched_skills"])
    print("Missing Skills:", result["missing_skills"])

    print("\nLearning Suggestions:")

    for item in result["learning_suggestions"]:
        print(f"{item['skill']}: {item['suggestion']}")

    print("\nCareer Development Roadmap:")

    for step_number, step in enumerate(result["roadmap"], start=1):
        print(f"{step_number}. {step}")

print("\nCAREER RECOMMENDATION TEST COMPLETED!")
