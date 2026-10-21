
import os
import re


SECTION_PATTERNS = {
    "Contact Information": r"\b(email|phone|contact|linkedin|github)\b",
    "Education": r"\b(education|academic|qualification)\b",
    "Skills": r"\b(skills|technical skills|technologies)\b",
    "Projects": r"\b(projects|academic projects|personal projects)\b",
    "Experience": r"\b(experience|internship|employment|work history)\b",
    "Summary / Objective": r"\b(summary|objective|professional profile)\b",
    "Certifications": r"\b(certifications|certificates|licenses)\b",
}

ACTION_VERBS = [
    "developed", "designed", "created", "implemented", "built",
    "analyzed", "managed", "improved", "automated", "optimized",
    "tested", "deployed", "collaborated", "integrated", "led",
    "maintained", "generated", "evaluated", "trained", "programmed",
    "engineered", "organized", "delivered", "reduced", "increased",
    "conducted", "researched", "predicted",
]

LEARNING_RESOURCES = {
    "python": ("Learn Python fundamentals, functions, and OOP.",
               "https://docs.python.org/3/tutorial/"),
    "java": ("Learn Java syntax, OOP, collections, and exceptions.",
             "https://dev.java/learn/"),
    "sql": ("Practise queries, joins, grouping, and subqueries.",
            "https://sqlbolt.com/"),
    "mysql": ("Learn database queries, joins, and table design.",
              "https://dev.mysql.com/doc/"),
    "pandas": ("Practise data cleaning and DataFrame operations.",
               "https://pandas.pydata.org/docs/getting_started/"),
    "numpy": ("Learn arrays and numerical computing.",
              "https://numpy.org/learn/"),
    "matplotlib": ("Create charts and visualise data.",
                   "https://matplotlib.org/stable/tutorials/"),
    "plotly": ("Create interactive charts and dashboards.",
               "https://plotly.com/python/"),
    "machine learning": ("Learn model training and evaluation.",
                         "https://scikit-learn.org/stable/tutorial/"),
    "scikit-learn": ("Practise preprocessing and machine learning.",
                     "https://scikit-learn.org/stable/tutorial/"),
    "deep learning": ("Learn neural networks and model training.",
                      "https://www.tensorflow.org/learn"),
    "tensorflow": ("Build and train neural networks.",
                   "https://www.tensorflow.org/tutorials"),
    "pytorch": ("Practise tensors and neural networks.",
                "https://pytorch.org/tutorials/"),
    "generative ai": ("Learn LLMs and generative AI fundamentals.",
                      "https://www.deeplearning.ai/short-courses/"),
    "llm": ("Learn language models and prompting.",
            "https://huggingface.co/learn"),
    "rag": ("Learn retrieval-augmented generation.",
            "https://python.langchain.com/docs/"),
    "nlp": ("Learn text processing and natural language processing.",
            "https://www.nltk.org/"),
    "html": ("Learn semantic HTML and page structure.",
             "https://developer.mozilla.org/en-US/docs/Learn/HTML"),
    "css": ("Learn responsive layouts, Flexbox, and Grid.",
            "https://developer.mozilla.org/en-US/docs/Learn/CSS"),
    "javascript": ("Learn JavaScript and browser interactions.",
                   "https://developer.mozilla.org/en-US/docs/Learn/JavaScript"),
    "react": ("Learn components, state, and hooks.",
              "https://react.dev/learn"),
    "node.js": ("Learn server-side JavaScript.",
                "https://nodejs.org/en/learn"),
    "rest api": ("Learn HTTP methods and API design.",
                 "https://developer.mozilla.org/en-US/docs/Web/HTTP"),
    "git": ("Learn version control, branches, and commits.",
            "https://git-scm.com/doc"),
    "docker": ("Learn containers and Dockerfiles.",
               "https://docs.docker.com/get-started/"),
    "aws": ("Learn cloud computing fundamentals.",
            "https://aws.amazon.com/training/"),
    "linux": ("Practise shell commands and file permissions.",
              "https://linuxjourney.com/"),
    "mongodb": ("Learn document databases and queries.",
                "https://learn.mongodb.com/"),
    "django": ("Build Python web applications.",
               "https://docs.djangoproject.com/en/stable/intro/"),
    "flask": ("Build web apps using Flask.",
              "https://flask.palletsprojects.com/en/stable/tutorial/"),
    "fastapi": ("Build Python APIs.",
                "https://fastapi.tiangolo.com/tutorial/"),
    "spring boot": ("Build Java applications and REST APIs.",
                    "https://spring.io/guides"),
    "c++": ("Learn C++ programming and OOP.",
            "https://www.learncpp.com/"),
    "power bi": ("Create reports and interactive dashboards.",
                 "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/"),
    "excel": ("Practise formulas, lookups, and pivot tables.",
              "https://support.microsoft.com/excel"),
    "tableau": ("Learn visual analytics and dashboards.",
                "https://www.tableau.com/learn/training"),
    "statistics": ("Learn probability and statistical analysis.",
                   "https://www.khanacademy.org/math/statistics-probability"),
    "typescript": ("Learn types and typed JavaScript.",
                   "https://www.typescriptlang.org/docs/"),
    "selenium": ("Practise browser automation.",
                 "https://www.selenium.dev/documentation/"),
    "pytest": ("Learn Python testing.",
               "https://docs.pytest.org/en/stable/"),
    "kubernetes": ("Learn containers and orchestration.",
                   "https://kubernetes.io/docs/tutorials/"),
    "postman": ("Practise API testing.",
                "https://learning.postman.com/"),
    "figma": ("Learn wireframes and interface design.",
              "https://help.figma.com/"),
}


def check_resume_quality(resume_text):
    text = resume_text or ""
    lower = text.lower()
    words = re.findall(r"\b[\w+#.-]+\b", text)
    checks = []

    for section, pattern in SECTION_PATTERNS.items():
        found = bool(re.search(pattern, lower))
        checks.append({
            "name": section,
            "passed": found,
            "details": "Section detected." if found
            else "Consider adding this section if relevant.",
        })

    word_count = len(words)
    length_ok = 150 <= word_count <= 1200
    checks.append({
        "name": "Resume Length",
        "passed": length_ok,
        "details": f"{word_count} words detected.",
    })

    found_verbs = [
        verb for verb in ACTION_VERBS
        if re.search(r"\b" + re.escape(verb) + r"\b", lower)
    ]
    action_count = len(found_verbs)
    checks.append({
        "name": "Action Verbs",
        "passed": action_count >= 3,
        "details": f"{action_count} different action verbs detected.",
    })

    metric_pattern = (
        r"\b\d+(?:\.\d+)?\s*(?:%|percent|users|records|projects|"
        r"hours|days|weeks|months|years|students|customers|"
        r"files|tests|seconds|minutes|models|datasets)\b"
    )
    metric_count = len(re.findall(metric_pattern, text, re.I))
    checks.append({
        "name": "Measurable Results",
        "passed": metric_count > 0,
        "details": f"{metric_count} measurable result(s) detected.",
    })

    score = round(
        sum(item["passed"] for item in checks) / len(checks) * 100
    )

    return {
        "score": score,
        "checks": checks,
        "word_count": word_count,
        "action_verb_count": action_count,
        "metric_count": metric_count,
        "note": "This is a basic resume quality estimate, not an official ATS score.",
    }


def create_learning_roadmap(missing_skills, target_role="Target role"):
    roadmap = []
    seen = set()

    for skill in missing_skills or []:
        skill = str(skill).strip()
        key = skill.lower()

        if not skill or key in seen:
            continue

        seen.add(key)
        learning_path, resource = LEARNING_RESOURCES.get(
            key,
            (
                f"Learn the fundamentals of {skill} and practise it "
                f"with a small {target_role} project.",
                "https://www.freecodecamp.org/learn/",
            ),
        )

        roadmap.append({
            "week": len(roadmap) + 1,
            "skill": skill,
            "learning_path": learning_path,
            "resource": resource,
            "task": (
                f"Complete one hands-on exercise in {skill} and build "
                f"a small project related to {target_role}."
            ),
        })

    return roadmap


def rule_based_resume_suggestions(resume_text, missing_skills):
    text = resume_text or ""
    lower = text.lower()
    suggestions = []

    for section, pattern in SECTION_PATTERNS.items():
        if not re.search(pattern, lower):
            suggestions.append(
                f"Consider adding a {section} section if relevant."
            )

    found_verbs = [
        verb for verb in ACTION_VERBS
        if re.search(r"\b" + re.escape(verb) + r"\b", lower)
    ]
    if len(found_verbs) < 3:
        suggestions.append(
            "Use accurate action verbs such as Developed, Designed, "
            "Implemented, and Analyzed to describe your contributions."
        )

    if not re.search(r"\b\d+(?:\.\d+)?\s*(?:%|users|records|projects|"
                     r"hours|days|students|tests)\b", text, re.I):
        suggestions.append(
            "Add real, verifiable project results or measurements where available. "
            "Do not invent numbers."
        )

    if missing_skills:
        suggestions.append(
            "Review skills not detected in your resume: "
            + ", ".join(str(s) for s in missing_skills[:10])
            + ". Learn and practise them before claiming proficiency."
        )

    if not suggestions:
        suggestions.append(
            "Tailor your resume to the job description and proofread it "
            "for clarity and accuracy."
        )

    return suggestions


def get_ai_suggestions(resume_text, job_description, missing_skills):
    api_key = os.getenv("GROQ_API_KEY", "")

    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            api_key = ""

    if not api_key:
        return {
            "mode": "Local rule-based suggestions",
            "suggestions": rule_based_resume_suggestions(
                resume_text, missing_skills
            ),
        }

    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        prompt = f"""
Review this resume for the target job.

JOB DESCRIPTION:
{(job_description or '')[:5000]}

RESUME:
{(resume_text or '')[:10000]}

SKILLS NOT DETECTED:
{', '.join(str(s) for s in (missing_skills or [])[:30])}

Give 6 concise, actionable suggestions. Never invent qualifications,
experience, or metrics. Return one suggestion per line.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a careful, honest resume reviewer.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1000,
        )

        content = response.choices[0].message.content or ""
        suggestions = [
            re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", line).strip()
            for line in content.splitlines()
            if line.strip()
        ]

        if suggestions:
            return {
                "mode": "Groq AI suggestions",
                "suggestions": suggestions,
            }

    except Exception:
        pass

    return {
        "mode": "Local fallback suggestions (AI unavailable)",
        "suggestions": rule_based_resume_suggestions(
            resume_text, missing_skills
        ),
    }
