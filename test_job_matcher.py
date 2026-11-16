
from ai_modules.job_matcher import calculate_job_matches

print("Starting Job Matching Test...")

results = calculate_job_matches(1)

print("\n===== JOB RECOMMENDATION RESULTS =====")

for job in results:
    print("\n------------------------------")
    print("Job:", job["job_title"])
    print("Company:", job["company_name"])
    print("Match:", str(job["match_percentage"]) + "%")
    print("Matched Skills:", job["matched_skills"])
    print("Missing Skills:", job["missing_skills"])

print("\n===== TEST COMPLETED =====")

