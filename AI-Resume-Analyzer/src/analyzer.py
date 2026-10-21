
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Skills expected for common Data Scientist jobs
ROLE_SKILLS = {
    "data scientist": [
        "Python", "SQL", "Statistics", "Probability",
        "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "Data Analysis", "Data Visualization",
        "Machine Learning", "Scikit-learn",
        "Feature Engineering", "Data Cleaning",
        "Exploratory Data Analysis", "Hypothesis Testing",
        "Regression", "Classification", "Clustering",
        "Deep Learning", "TensorFlow", "PyTorch",
        "Jupyter Notebook", "Excel", "Power BI",
        "Tableau", "Git", "Problem Solving"
    ],
    "python developer": [
        "Python", "OOP", "SQL", "Git", "REST API",
        "Flask", "Django", "FastAPI", "Testing",
        "Data Structures", "Algorithms", "Linux"
    ],
    "ai/ml engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "Scikit-learn", "TensorFlow", "PyTorch",
        "NumPy", "Pandas", "Statistics",
        "Feature Engineering", "NLP", "Computer Vision",
        "Model Evaluation", "Git", "SQL"
    ],
    "web developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Node.js", "REST API", "SQL", "Git",
        "Responsive Design", "Testing"
    ],
    "java developer": [
        "Java", "OOP", "Data Structures", "Algorithms",
        "SQL", "Spring Boot", "REST API", "Git",
        "Maven", "Testing"
    ]
}

# Alternate names for common skills
ALIASES = {
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "js": "javascript",
    "postgres": "postgresql",
    "powerbi": "power bi",
    "jupyter": "jupyter notebook",
    "ml": "machine learning",
    "eda": "exploratory data analysis",
    "natural language processing": "nlp",
    "object oriented programming": "oop",
    "data visualisation": "data visualization",
    "data analytics": "data analysis",
    "data manipulation": "pandas",
    "numerical python": "numpy"
}


def normalize_text(text):
    """Normalize text and common skill aliases."""
    text = str(text or "").lower()
    text = text.replace("scikit‑learn", "scikit-learn")
    text = text.replace("nodejs", "node.js")
    text = re.sub(r"\s+", " ", text).strip()

    for alias, canonical in ALIASES.items():
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
        text = re.sub(pattern, canonical, text)

    return text


def extract_skills(text, skills):
    """Find skills in resume text using word boundaries."""
    normalized = normalize_text(text)
    found = []

    for skill in skills:
        normalized_skill = normalize_text(skill)
        pattern = r"(?<!\w)" + re.escape(normalized_skill) + r"(?!\w)"

        if re.search(pattern, normalized):
            found.append(skill)

    return list(dict.fromkeys(found))


def calculate_similarity(resume_text, job_text):
    """Calculate TF-IDF text similarity, safely handling empty text."""
    resume_text = str(resume_text or "").strip()
    job_text = str(job_text or "").strip()

    if not resume_text or not job_text:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        vectors = vectorizer.fit_transform([resume_text, job_text])
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

        return round(float(score) * 100, 2)

    except ValueError:
        return 0.0


def analyze_resume(resume_text, job_role="Data Scientist",
                   job_description=""):
    """
    Analyze a resume against a selected job role.

    Returns matching/missing skills, skill match percentage,
    and text similarity for the dashboard and charts.
    """
    resume_text = str(resume_text or "").strip()
    role_key = normalize_text(job_role)

    # Select the appropriate role skills.
    required_skills = ROLE_SKILLS.get(
        role_key,
        ROLE_SKILLS["data scientist"]
    )

    # Find skills actually mentioned in the resume.
    resume_skills = extract_skills(resume_text, required_skills)

    matching_skills = [
        skill for skill in required_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in matching_skills
    ]

    # Compare the resume with the role's requirements.
    if job_description and job_description.strip():
        target_text = job_description
    else:
        target_text = (
            f"{job_role} responsibilities and required skills. "
            + ", ".join(required_skills)
        )

    similarity_score = calculate_similarity(
        resume_text, target_text
    )

    # Skill match is based on detected required skills.
    skill_match_score = round(
        len(matching_skills) / len(required_skills) * 100, 2
    ) if required_skills else 0.0

    # A simple, transparent composite score for the dashboard.
    overall_score = round(
        0.7 * skill_match_score + 0.3 * similarity_score, 2
    )

    return {
        "job_role": job_role,
        "similarity_score": similarity_score,
        "job_similarity": similarity_score,
        "skill_match_score": skill_match_score,
        "overall_score": overall_score,
        "resume_score": overall_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "job_skills": required_skills,
        "required_skills": required_skills,
        "total_required_skills": len(required_skills),
        "total_matching_skills": len(matching_skills)
    }
