
import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote_plus

from src.resume_parser import extract_resume_text
from src.analyzer import analyze_resume
from src.upgrade import (
    check_resume_quality,
    create_learning_roadmap,
    get_ai_suggestions,
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# LARGE FONT AND PROFESSIONAL STYLING
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fb;
    }

    html, body, [class*="css"] {
        font-size: 20px !important;
    }

    p, li, label, .stMarkdown {
        font-size: 20px !important;
        line-height: 1.7 !important;
    }

    h1 {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #17365d !important;
    }

    h2 {
        font-size: 32px !important;
        color: #17365d !important;
    }

    h3 {
        font-size: 25px !important;
        color: #234e70 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #eaf0f8;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        font-size: 18px !important;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #dbe4f0;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 18px !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: bold !important;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        font-size: 18px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        min-height: 48px;
    }

    div[data-testid="stTabs"] button {
        font-size: 18px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
    }

    a {
        font-size: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# COURSE LINKS FOR SKILLS
# ============================================================

COURSE_LINKS = {
    "python": (
        "Python for Beginners",
        "freeCodeCamp",
        "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
    ),
    "java": (
        "Java Programming",
        "Oracle",
        "https://dev.java/learn/",
    ),
    "sql": (
        "SQL Fundamentals",
        "SQLBolt",
        "https://sqlbolt.com/",
    ),
    "mysql": (
        "MySQL Tutorials",
        "MySQL Documentation",
        "https://dev.mysql.com/doc/",
    ),
    "pandas": (
        "Pandas for Data Analysis",
        "Pandas Documentation",
        "https://pandas.pydata.org/docs/getting_started/",
    ),
    "numpy": (
        "NumPy Learning Resources",
        "NumPy",
        "https://numpy.org/learn/",
    ),
    "matplotlib": (
        "Data Visualization with Matplotlib",
        "Matplotlib",
        "https://matplotlib.org/stable/tutorials/",
    ),
    "plotly": (
        "Interactive Data Visualization",
        "Plotly",
        "https://plotly.com/python/",
    ),
    "data visualization": (
        "Data Visualization with Python",
        "Plotly",
        "https://plotly.com/python/",
    ),
    "statistics": (
        "Statistics and Probability",
        "Khan Academy",
        "https://www.khanacademy.org/math/statistics-probability",
    ),
    "machine learning": (
        "Machine Learning Specialization",
        "DeepLearning.AI",
        "https://www.coursera.org/specializations/machine-learning-introduction",
    ),
    "scikit-learn": (
        "Machine Learning Tutorials",
        "Scikit-learn",
        "https://scikit-learn.org/stable/tutorial/index.html",
    ),
    "deep learning": (
        "Deep Learning Courses",
        "DeepLearning.AI",
        "https://www.deeplearning.ai/courses/",
    ),
    "tensorflow": (
        "TensorFlow Tutorials",
        "TensorFlow",
        "https://www.tensorflow.org/tutorials",
    ),
    "pytorch": (
        "PyTorch Tutorials",
        "PyTorch",
        "https://pytorch.org/tutorials/",
    ),
    "nlp": (
        "Natural Language Processing",
        "Hugging Face",
        "https://huggingface.co/learn/nlp-course/",
    ),
    "natural language processing": (
        "Natural Language Processing",
        "Hugging Face",
        "https://huggingface.co/learn/nlp-course/",
    ),
    "generative ai": (
        "Generative AI Learning Resources",
        "Google Cloud Skills Boost",
        "https://www.cloudskillsboost.google/",
    ),
    "llm": (
        "Large Language Models",
        "Hugging Face",
        "https://huggingface.co/learn",
    ),
    "html": (
        "Learn HTML",
        "MDN Web Docs",
        "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content",
    ),
    "css": (
        "Learn CSS",
        "MDN Web Docs",
        "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics",
    ),
    "javascript": (
        "JavaScript Guide",
        "MDN Web Docs",
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
    ),
    "react": (
        "Learn React",
        "React Documentation",
        "https://react.dev/learn",
    ),
    "node.js": (
        "Node.js Learning Resources",
        "Node.js",
        "https://nodejs.org/en/learn",
    ),
    "nodejs": (
        "Node.js Learning Resources",
        "Node.js",
        "https://nodejs.org/en/learn",
    ),
    "rest api": (
        "REST API Fundamentals",
        "Postman Learning Center",
        "https://learning.postman.com/",
    ),
    "git": (
        "Git Learning Resources",
        "Git Documentation",
        "https://git-scm.com/doc",
    ),
    "docker": (
        "Docker Getting Started",
        "Docker",
        "https://docs.docker.com/get-started/",
    ),
    "aws": (
        "Cloud Computing Learning",
        "AWS Skill Builder",
        "https://skillbuilder.aws/",
    ),
    "power bi": (
        "Power BI Learning",
        "Microsoft Learn",
        "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/",
    ),
    "excel": (
        "Excel Training",
        "Microsoft Support",
        "https://support.microsoft.com/en-us/excel",
    ),
    "mongodb": (
        "MongoDB Learning Resources",
        "MongoDB University",
        "https://learn.mongodb.com/",
    ),
    "django": (
        "Django Tutorials",
        "Django Documentation",
        "https://docs.djangoproject.com/en/stable/intro/tutorial01/",
    ),
    "flask": (
        "Flask Quickstart",
        "Flask Documentation",
        "https://flask.palletsprojects.com/en/stable/quickstart/",
    ),
    "fastapi": (
        "FastAPI Tutorial",
        "FastAPI Documentation",
        "https://fastapi.tiangolo.com/tutorial/",
    ),
    "c++": (
        "Learn C++",
        "LearnCpp.com",
        "https://www.learncpp.com/",
    ),
    "linux": (
        "Linux Command Line",
        "Linux Journey",
        "https://linuxjourney.com/",
    ),
    "typescript": (
        "TypeScript Handbook",
        "TypeScript Documentation",
        "https://www.typescriptlang.org/docs/handbook/intro.html",
    ),
    "selenium": (
        "Selenium Browser Automation",
        "Selenium Documentation",
        "https://www.selenium.dev/documentation/",
    ),
    "kubernetes": (
        "Kubernetes Basics",
        "Kubernetes Documentation",
        "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
    ),
}

# ============================================================
# REFERENCES TO READ
# ============================================================

REFERENCES = [
    (
        "Streamlit Documentation",
        "Learn dashboards, layouts, tabs, file uploads, and metrics.",
        "https://docs.streamlit.io/",
    ),
    (
        "Python Official Tutorial",
        "Learn Python functions, lists, dictionaries, and modules.",
        "https://docs.python.org/3/tutorial/",
    ),
    (
        "Plotly Python Documentation",
        "Learn interactive charts, chart formatting, and visualization.",
        "https://plotly.com/python/",
    ),
    (
        "CSS Styling Basics",
        "Learn fonts, colors, spacing, and responsive design.",
        "https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics",
    ),
    (
        "PDFPlumber Documentation",
        "Learn how text is extracted from PDF resumes.",
        "https://github.com/jsvine/pdfplumber",
    ),
    (
        "Scikit-learn Documentation",
        "Learn text processing, TF-IDF, and machine learning.",
        "https://scikit-learn.org/stable/",
    ),
    (
        "Groq Documentation",
        "Learn how to connect AI models to an application.",
        "https://console.groq.com/docs/overview",
    ),
]

# ============================================================
# JOB ROLES AND DEFAULT SKILLS
# ============================================================

ROLE_SKILLS = {
    "Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Statistics",
        "Machine Learning",
        "Scikit-learn",
        "Data Visualization",
    ],
    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Generative AI",
        "LLM",
        "SQL",
        "Git",
    ],
    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "SQL",
        "Git",
    ],
    "Python Developer": [
        "Python",
        "SQL",
        "Git",
        "REST API",
        "Django",
        "Flask",
    ],
    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Git",
        "REST API",
    ],
    "Java Developer": [
        "Java",
        "SQL",
        "Git",
        "REST API",
    ],
    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Pandas",
        "Statistics",
        "Power BI",
        "Data Visualization",
    ],
    "Full Stack Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "SQL",
        "Git",
        "REST API",
    ],
    "Cloud Engineer": [
        "AWS",
        "Linux",
        "Docker",
        "Kubernetes",
        "Git",
        "Python",
    ],
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_first(data, keys, default=None):
    """Return the first available value from a dictionary."""
    if not isinstance(data, dict):
        return default

    for key in keys:
        if key in data and data[key] is not None:
            return data[key]

    return default


def normalize_skills(skills):
    """Convert skill results into a clean list of strings."""
    if skills is None:
        return []

    if isinstance(skills, str):
        return [
            item.strip()
            for item in skills.split(",")
            if item.strip()
        ]

    if isinstance(skills, dict):
        return [
            str(key).strip()
            for key, value in skills.items()
            if value and str(key).strip()
        ]

    try:
        return [
            str(skill).strip()
            for skill in skills
            if str(skill).strip()
        ]
    except TypeError:
        return []


def as_percentage(value):
    """Convert a score in either 0-1 or 0-100 format to percent."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0

    if 0 <= number <= 1:
        number *= 100

    return max(0.0, min(100.0, number))


def get_course(skill):
    """Return a known course or a relevant online search link."""
    key = skill.strip().lower()

    if key in COURSE_LINKS:
        title, provider, url = COURSE_LINKS[key]
        return title, provider, url

    # Try a partial match for skills with slightly different names.
    for known_skill, course in COURSE_LINKS.items():
        if known_skill in key or key in known_skill:
            return course

    search_url = (
        "https://www.google.com/search?q="
        + quote_plus(skill + " free online course")
    )

    return (
        f"Learn {skill}",
        "Online learning resources",
        search_url,
    )


def make_chart(data, x, y, title, color, height=430):
    """Create a large, readable Plotly bar chart."""
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=[color],
        text=y,
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=16),
        cliponaxis=False,
    )

    fig.update_layout(
        height=height,
        autosize=True,
        margin=dict(l=35, r=35, t=80, b=65),
        font=dict(
            family="Arial",
            size=16,
            color="#1e293b",
        ),
        title_font=dict(size=23),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            tickfont=dict(size=15),
            title_font=dict(size=17),
        ),
        yaxis=dict(
            tickfont=dict(size=15),
            title_font=dict(size=17),
            range=[0, 110],
        ),
        showlegend=False,
    )

    return fig


# ============================================================
# HEADER
# ============================================================

st.title("📄 AI Resume Analyzer")

st.markdown(
    """
    Analyze your resume, compare it with a job role, identify missing
    skills, explore recommended courses, and improve your job readiness.
    """
)

st.divider()

# ============================================================
# SIDEBAR INPUTS
# ============================================================

st.sidebar.title("⚙️ Resume Analysis Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
)

job_roles = list(ROLE_SKILLS.keys())

selected_role = st.sidebar.selectbox(
    "Select your target job role",
    job_roles,
    index=0,
)

st.sidebar.markdown("### 📝 Job Description")

st.sidebar.caption(
    "Paste the job description from a job posting. "
    "If you leave it empty, the app uses a basic skill profile "
    "for your selected role."
)

job_description_input = st.sidebar.text_area(
    "Job description",
    height=180,
    placeholder="Paste the job description here...",
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Your results depend on the text extracted from your PDF "
    "and the job requirements used for comparison."
)

# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "🔍 Analyze My Resume",
    type="primary",
    use_container_width=True,
)

if analyze_button:
    if uploaded_file is None:
        st.error("Please upload your resume in PDF format first.")

    else:
        try:
            with st.spinner("Reading and analyzing your resume..."):
                uploaded_file.seek(0)
                resume_text = extract_resume_text(uploaded_file)

                if not resume_text or not resume_text.strip():
                    st.error(
                        "No readable text was found in the PDF. "
                        "Please upload a text-based PDF rather than "
                        "a scanned image PDF."
                    )
                    st.stop()

                # Use the supplied job description if available.
                # Otherwise, use a role-specific default skill profile.
                if job_description_input.strip():
                    job_description = job_description_input.strip()
                else:
                    role_skills = ROLE_SKILLS[selected_role]
                    job_description = (
                        f"Job role: {selected_role}. "
                        f"Required skills: {', '.join(role_skills)}. "
                        f"Candidates should demonstrate relevant "
                        f"technical knowledge and practical project experience."
                    )

                analysis = analyze_resume(
                    resume_text,
                    job_description,
                )

                if not isinstance(analysis, dict):
                    raise ValueError(
                        "The analyzer did not return the expected results."
                    )

                similarity = as_percentage(
                    get_first(
                        analysis,
                        ["similarity_score", "job_similarity_score"],
                        0,
                    )
                )

                skill_match = as_percentage(
                    get_first(
                        analysis,
                        ["skill_match_score", "skills_match_score"],
                        0,
                    )
                )

                matching_skills = normalize_skills(
                    get_first(
                        analysis,
                        ["matching_skills", "matched_skills"],
                        [],
                    )
                )

                missing_skills = normalize_skills(
                    get_first(
                        analysis,
                        ["missing_skills", "skills_to_learn"],
                        [],
                    )
                )

                resume_skills = normalize_skills(
                    get_first(
                        analysis,
                        ["resume_skills", "extracted_skills"],
                        [],
                    )
                )

                job_skills = normalize_skills(
                    get_first(
                        analysis,
                        ["job_skills", "required_skills"],
                        ROLE_SKILLS[selected_role],
                    )
                )

                # Ensure the course section has useful role-specific
                # recommendations even if the analyzer misses a skill.
                if not job_description_input.strip():
                    resume_skill_names = {
                        skill.lower() for skill in resume_skills
                    }
                    matching_names = {
                        skill.lower() for skill in matching_skills
                    }

                    for skill in ROLE_SKILLS[selected_role]:
                        if (
                            skill.lower() not in resume_skill_names
                            and skill.lower() not in matching_names
                            and skill.lower()
                            not in {item.lower() for item in missing_skills}
                        ):
                            missing_skills.append(skill)

                quality = check_resume_quality(resume_text)

                quality_score = as_percentage(
                    get_first(quality, ["score"], 0)
                )

                word_count = get_first(
                    quality,
                    ["word_count"],
                    len(resume_text.split()),
                )

                # Generate the roadmap.
                try:
                    roadmap = create_learning_roadmap(
                        missing_skills,
                        selected_role,
                    )
                except Exception:
                    roadmap = []

                # Generate suggestions, using the existing upgrade.py.
                try:
                    suggestions = get_ai_suggestions(
                        resume_text,
                        job_description,
                        missing_skills,
                    )
                except Exception as error:
                    suggestions = (
                        "AI suggestions could not be generated. "
                        "Please check your AI API configuration if "
                        "you want AI-powered feedback. "
                        f"Details: {error}"
                    )

                # Save all results for displaying across tabs.
                st.session_state["resume_results"] = {
                    "resume_text": resume_text,
                    "analysis": analysis,
                    "similarity": similarity,
                    "skill_match": skill_match,
                    "matching_skills": matching_skills,
                    "missing_skills": missing_skills,
                    "resume_skills": resume_skills,
                    "job_skills": job_skills,
                    "quality": quality,
                    "quality_score": quality_score,
                    "word_count": word_count,
                    "roadmap": roadmap,
                    "suggestions": suggestions,
                    "selected_role": selected_role,
                    "job_description": job_description,
                }

            st.success("Resume analysis completed successfully!")

        except Exception as error:
            st.error(
                "Something went wrong while analyzing the resume."
            )
            st.exception(error)

# ============================================================
# DISPLAY RESULTS
# ============================================================

if "resume_results" in st.session_state:
    results = st.session_state["resume_results"]

    resume_text = results["resume_text"]
    similarity = results["similarity"]
    skill_match = results["skill_match"]
    matching_skills = results["matching_skills"]
    missing_skills = results["missing_skills"]
    resume_skills = results["resume_skills"]
    job_skills = results["job_skills"]
    quality = results["quality"]
    quality_score = results["quality_score"]
    word_count = results["word_count"]
    roadmap = results["roadmap"]
    suggestions = results["suggestions"]
    selected_role = results["selected_role"]

    st.divider()
    st.header("📊 Resume Analysis Dashboard")
    st.write(f"**Selected job role:** {selected_role}")

    # --------------------------------------------------------
    # SUMMARY METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Job Similarity",
            f"{similarity:.1f}%",
        )

    with col2:
        st.metric(
            "Skill Match",
            f"{skill_match:.1f}%",
        )

    with col3:
        st.metric(
            "Resume Quality",
            f"{quality_score:.1f}%",
        )

    with col4:
        st.metric(
            "Words in Resume",
            str(word_count),
        )

    st.caption(
        "Similarity and skill-match scores are estimates based on "
        "the text and skill rules used by this application. "
        "They are not guarantees of ATS results or interview selection."
    )

    # --------------------------------------------------------
    # SKILL MATCHING
    # --------------------------------------------------------

    st.divider()
    st.header("🧠 Skill Matching Results")

    skill_col1, skill_col2 = st.columns(2)

    with skill_col1:
        st.subheader("✅ Matching Skills")

        if matching_skills:
            for skill in matching_skills:
                st.markdown(f"- ✅ {skill}")
        else:
            st.info(
                "No matching skills were identified. "
                "Check the resume text and job description."
            )

    with skill_col2:
        st.subheader("📌 Skills to Improve")

        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"- 📘 {skill}")
        else:
            st.success(
                "No missing skills were reported by the current analyzer."
            )

    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    st.divider()
    st.header("📈 Visual Analysis")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        score_df = pd.DataFrame(
            {
                "Category": [
                    "Job Similarity",
                    "Skill Match",
                    "Resume Quality",
                ],
                "Score": [
                    similarity,
                    skill_match,
                    quality_score,
                ],
            }
        )

        fig_scores = make_chart(
            score_df,
            x="Category",
            y="Score",
            title="Resume Performance Scores",
            color="#3478c7",
            height=450,
        )

        fig_scores.update_layout(
            yaxis=dict(
                title="Score (%)",
                range=[0, 110],
                tickfont=dict(size=14),
            )
        )

        st.plotly_chart(
            fig_scores,
            use_container_width=True,
            config={
                "responsive": True,
                "displayModeBar": False,
            },
        )

    with chart_col2:
        matched_count = len(matching_skills)
        missing_count = len(missing_skills)

        if matched_count + missing_count > 0:
            skills_df = pd.DataFrame(
                {
                    "Skill Status": [
                        "Matching Skills",
                        "Missing Skills",
                    ],
                    "Count": [
                        matched_count,
                        missing_count,
                    ],
                }
            )

            fig_skills = px.pie(
                skills_df,
                names="Skill Status",
                values="Count",
                title="Matching vs Missing Skills",
                hole=0.45,
                color_discrete_sequence=[
                    "#16a085",
                    "#e67e22",
                ],
            )

            fig_skills.update_traces(
                textposition="inside",
                textinfo="label+value+percent",
                textfont_size=16,
            )

            fig_skills.update_layout(
                height=450,
                autosize=True,
                margin=dict(l=25, r=25, t=75, b=35),
                font=dict(
                    family="Arial",
                    size=16,
                    color="#1e293b",
                ),
                title_font=dict(size=23),
                paper_bgcolor="white",
                plot_bgcolor="white",
                legend=dict(font=dict(size=15)),
            )

            st.plotly_chart(
                fig_skills,
                use_container_width=True,
                config={
                    "responsive": True,
                    "displayModeBar": False,
                },
            )
        else:
            st.info(
                "The skill chart will appear when skills are identified."
            )

    # ========================================================
    # COURSE RECOMMENDATIONS
    # ========================================================

    st.divider()
    st.header("🎓 Recommended Courses to Learn Missing Skills")

    st.write(
        "Use these resources to work on the skills identified as "
        "missing for your selected job role. Course availability, "
        "pricing, and certificates depend on the provider."
    )

    if missing_skills:
        for index, skill in enumerate(missing_skills, start=1):
            course_title, provider, course_url = get_course(skill)

            with st.container(border=True):
                st.subheader(f"{index}. 📘 {skill}")
                st.write(f"**Suggested learning resource:** {course_title}")
                st.write(f"**Provider:** {provider}")

                st.link_button(
                    "🎯 Start Learning",
                    course_url,
                    use_container_width=False,
                )

    else:
        st.success(
            "The analyzer did not identify missing skills for this "
            "comparison. You can still explore the references below "
            "or provide a more detailed job description."
        )

    # ========================================================
    # TABS FOR ADDITIONAL FEATURES
    # ========================================================

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📝 Resume Quality",
            "🗺️ Learning Roadmap",
            "🤖 AI Suggestions",
            "📄 Extracted Resume",
            "📚 References to Read",
        ]
    )

    # --------------------------------------------------------
    # TAB 1: RESUME QUALITY
    # --------------------------------------------------------

    with tab1:
        st.subheader("📝 Resume Quality Checker")

        checks = get_first(
            quality,
            ["checks"],
            {},
        )

        if isinstance(checks, dict):
            for check_name, check_result in checks.items():
                if isinstance(check_result, bool):
                    if check_result:
                        st.success(f"✅ {check_name}")
                    else:
                        st.warning(f"⚠️ {check_name}")
                else:
                    st.write(f"**{check_name}:** {check_result}")

        elif isinstance(checks, list):
            for check in checks:
                st.write(f"• {check}")

        st.write(
            f"**Word count:** {word_count}"
        )

        st.write(
            f"**Action verbs detected:** "
            f"{get_first(quality, ['action_verb_count'], 'N/A')}"
        )

        st.write(
            f"**Metrics or numbers detected:** "
            f"{get_first(quality, ['metric_count'], 'N/A')}"
        )

        quality_note = get_first(quality, ["note"])

        if quality_note:
            st.info(str(quality_note))

    # --------------------------------------------------------
    # TAB 2: LEARNING ROADMAP
    # --------------------------------------------------------

    with tab2:
        st.subheader("🗺️ Your Learning Roadmap")

        if roadmap:
            if isinstance(roadmap, list):
                for item in roadmap:
                    if isinstance(item, dict):
                        week = item.get("week", "Learning Plan")
                        skill = item.get("skill", "")
                        learning_path = item.get("learning_path", "")
                        resource = item.get("resource", "")
                        task = item.get("task", "")

                        with st.container(border=True):
                            st.markdown(f"### 📅 {week}")
                            if skill:
                                st.write(f"**Skill:** {skill}")
                            if learning_path:
                                st.write(
                                    f"**Learning path:** {learning_path}"
                                )
                            if resource:
                                st.write(f"**Resource:** {resource}")
                            if task:
                                st.write(f"**Practice task:** {task}")

                    else:
                        st.write(str(item))

            else:
                st.write(str(roadmap))

        else:
            st.info(
                "A learning roadmap will appear here when missing "
                "skills are available."
            )

    # --------------------------------------------------------
    # TAB 3: AI SUGGESTIONS
    # --------------------------------------------------------

    with tab3:
        st.subheader("🤖 Resume Improvement Suggestions")

        if isinstance(suggestions, (list, tuple)):
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
        elif isinstance(suggestions, dict):
            for title, suggestion in suggestions.items():
                st.markdown(f"**{title}**")
                st.write(str(suggestion))
        else:
            st.write(str(suggestions))

    # --------------------------------------------------------
    # TAB 4: EXTRACTED RESUME
    # --------------------------------------------------------

    with tab4:
        st.subheader("📄 Text Extracted from Your Resume")

        st.caption(
            "Review the extracted text to make sure your PDF was read correctly."
        )

        st.text_area(
            "Resume text",
            value=resume_text,
            height=400,
            disabled=True,
        )

        st.download_button(
            "⬇️ Download Extracted Resume Text",
            data=resume_text,
            file_name="extracted_resume.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # TAB 5: REFERENCES TO READ
    # --------------------------------------------------------

    with tab5:
        st.subheader("📚 References to Read")

        st.write(
            "Explore these official documentation pages to understand "
            "the tools and technologies used in your resume analyzer."
        )

        for index, reference in enumerate(REFERENCES, start=1):
            title, description, url = reference

            with st.container(border=True):
                st.markdown(f"### {index}. {title}")
                st.write(description)

                st.link_button(
                    "📖 Read Documentation",
                    url,
                    use_container_width=False,
                )

    # ========================================================
    # DOWNLOAD REPORTS
    # ========================================================

    st.divider()
    st.header("⬇️ Download Your Results")

    report_data = {
        "Selected Job Role": selected_role,
        "Job Similarity (%)": round(similarity, 2),
        "Skill Match (%)": round(skill_match, 2),
        "Resume Quality (%)": round(quality_score, 2),
        "Word Count": word_count,
        "Matching Skills": ", ".join(matching_skills),
        "Missing Skills": ", ".join(missing_skills),
    }

    report_df = pd.DataFrame(
        list(report_data.items()),
        columns=["Metric", "Result"],
    )

    download_col1, download_col2 = st.columns(2)

    with download_col1:
        st.download_button(
            "📊 Download Analysis Report (CSV)",
            data=report_df.to_csv(index=False).encode("utf-8"),
            file_name="resume_analysis_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with download_col2:
        course_rows = []

        for skill in missing_skills:
            title, provider, url = get_course(skill)

            course_rows.append(
                {
                    "Missing Skill": skill,
                    "Suggested Resource": title,
                    "Provider": provider,
                    "Course Link": url,
                }
            )

        course_df = pd.DataFrame(
            course_rows,
            columns=[
                "Missing Skill",
                "Suggested Resource",
                "Provider",
                "Course Link",
            ],
        )

        st.download_button(
            "🎓 Download Course Recommendations (CSV)",
            data=course_df.to_csv(index=False).encode("utf-8"),
            file_name="recommended_courses.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:15px; color:#64748b;">
        <p><strong>AI Resume Analyzer</strong></p>
        <p>Analyze your skills. Learn what is missing. Prepare for your next opportunity.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
