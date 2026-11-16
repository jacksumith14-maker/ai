
# Career Recommendation and Skill Gap Analysis

CAREER_PATHS = [
    {
        "career": "Frontend Developer",
        "description": "Develop websites and user interfaces.",
        "required_skills": [
            "html", "css", "javascript", "react", "git"
        ]
    },
    {
        "career": "Backend Developer",
        "description": "Build server-side applications and APIs.",
        "required_skills": [
            "python", "flask", "django", "mysql", "sql", "git"
        ]
    },
    {
        "career": "Full Stack Developer",
        "description": "Work with both frontend and backend technologies.",
        "required_skills": [
            "html", "css", "javascript", "react",
            "python", "flask", "mysql", "git"
        ]
    },
    {
        "career": "Data Analyst",
        "description": "Analyze data and generate useful insights.",
        "required_skills": [
            "python", "sql", "mysql", "excel",
            "power bi", "statistics"
        ]
    },
    {
        "career": "Java Developer",
        "description": "Develop applications using Java programming.",
        "required_skills": [
            "java", "sql", "mysql", "git"
        ]
    }
]


# Personalized Learning Suggestions

SKILL_LEARNING_SUGGESTIONS = {
    "python": "Learn variables, loops, functions and OOP. Practise by building a small Python program.",
    "flask": "Learn Flask routes, templates and forms. Practise by creating a simple web application.",
    "django": "Learn Django models, views and URLs. Practise by building a student management application.",
    "java": "Learn Java syntax, classes and OOP. Practise by creating a simple Java application.",
    "html": "Learn HTML elements, forms and semantic tags. Practise by creating a portfolio page.",
    "css": "Learn selectors, flexbox and responsive design. Practise by styling your portfolio.",
    "javascript": "Learn variables, functions and DOM manipulation. Practise by creating an interactive webpage.",
    "react": "Learn components, props and useState. Practise by building a small React application.",
    "mysql": "Learn SQL queries, joins and database relationships. Practise by creating a database project.",
    "sql": "Learn SELECT, INSERT, UPDATE, DELETE and JOIN queries. Practise with sample databases.",
    "git": "Learn Git commands, commits and branches. Practise by managing a project using Git.",
    "excel": "Learn formulas, sorting, filtering and pivot tables. Practise by analysing sample data.",
    "power bi": "Learn data import, visualizations and dashboards. Practise by creating a sales dashboard.",
    "statistics": "Learn mean, median, mode and basic probability. Practise by analysing a small dataset."
}


# Career Development Roadmaps

CAREER_ROADMAPS = {
    "Frontend Developer": [
        "Learn HTML fundamentals and semantic elements.",
        "Learn CSS, Flexbox and responsive design.",
        "Learn JavaScript fundamentals and DOM manipulation.",
        "Learn React components, props and state.",
        "Build a responsive portfolio website."
    ],

    "Backend Developer": [
        "Learn Python programming fundamentals.",
        "Learn Flask or Django framework basics.",
        "Learn MySQL and database management.",
        "Learn how to create REST APIs.",
        "Build a backend application connected to MySQL."
    ],

    "Full Stack Developer": [
        "Learn HTML, CSS and JavaScript.",
        "Learn Python programming fundamentals.",
        "Learn Flask routes, templates and forms.",
        "Learn MySQL database integration.",
        "Connect frontend and backend components.",
        "Build a complete Full Stack web application."
    ],

    "Data Analyst": [
        "Learn Excel formulas and data handling.",
        "Learn Python for data analysis.",
        "Learn SQL queries and database operations.",
        "Study statistics and data interpretation.",
        "Learn Power BI dashboards and visualizations.",
        "Build a data analysis project."
    ],

    "Java Developer": [
        "Learn Java programming fundamentals.",
        "Understand object-oriented programming.",
        "Learn Java collections and exception handling.",
        "Learn SQL and MySQL database connectivity.",
        "Build a Java application connected to MySQL."
    ]
}


def recommend_careers(resume_skills):

    # Convert resume skills into lowercase
    user_skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    recommendations = []

    for path in CAREER_PATHS:

        required_skills = set(path["required_skills"])

        # Identify matched skills
        matched_skills = user_skills.intersection(
            required_skills
        )

        # Identify missing skills
        missing_skills = required_skills - user_skills

        # Calculate career match percentage
        match_percentage = round(
            len(matched_skills) /
            len(required_skills) * 100
        )

        # Generate personalized learning suggestions
        learning_suggestions = [
            {
                "skill": skill,
                "suggestion": SKILL_LEARNING_SUGGESTIONS.get(
                    skill,
                    f"Learn the fundamentals of {skill} and practise with a small project."
                )
            }
            for skill in sorted(missing_skills)
        ]

        # Get career development roadmap
        career_roadmap = CAREER_ROADMAPS.get(
            path["career"], []
        )

        recommendations.append({
            "career": path["career"],
            "description": path["description"],
            "match_percentage": match_percentage,
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(missing_skills),
            "learning_suggestions": learning_suggestions,
            "roadmap": career_roadmap
        })

    # Show highest matching careers first
    recommendations.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    return recommendations
