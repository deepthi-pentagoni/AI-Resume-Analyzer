import re
import streamlit as st
from resume_parser import extract_text_from_pdf
from gemini_analyzer import analyze_resume

def calculate_match(resume_text, job_role):

    resume = resume_text.lower()

    skills = {
        "Software Engineer": [
            "python", "java", "c++", "sql", "git", "oop"
        ],
        "Data Scientist": [
            "python", "pandas", "numpy",
            "machine learning", "sql", "statistics"
        ],
        "AI Engineer": [
            "python", "tensorflow", "pytorch",
            "llm", "transformers", "huggingface"
        ],
        "Machine Learning Engineer": [
            "python", "scikit", "tensorflow",
            "pytorch", "ml"
        ],
        "Frontend Developer": [
            "html", "css", "javascript",
            "react", "bootstrap"
        ],
        "Backend Developer": [
            "python", "django", "flask",
            "api", "sql"
        ],
        "Cyber Security": [
            "network", "linux",
            "wireshark", "nmap", "security"
        ],
        "Cloud Engineer": [
            "aws", "azure",
            "docker", "kubernetes", "linux"
        ]
    }

    required = skills.get(job_role, [])

    found = sum(skill in resume for skill in required)

    if len(required) == 0:
        return 0

    return int(found / len(required) * 100)


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.image("assets/logo.png", width=120)

with st.sidebar:

    st.title("📄 AI Resume Analyzer")

    st.markdown("""
### Features

✅ ATS Score

✅ Resume Match

✅ AI Suggestions

✅ Missing Skills

✅ Resume Statistics

✅ Resume Completeness
""")

    st.divider()

    st.info(
        """
Upload your resume and receive AI-powered feedback,
ATS compatibility, missing skills, resume statistics,
and personalized suggestions.
"""
    )

    st.divider()

    st.metric("AI Model", "Llama 3.3")

    st.metric("Framework", "Streamlit")

    st.metric("Language", "Python")


st.markdown("""
# 📄 AI Resume Analyzer

### Analyze your resume using AI

Upload a PDF resume and receive:

- 🎯 ATS Score
- 📈 Resume Match
- 🛠 Skill Detection
- 💡 AI Suggestions
- 📊 Resume Statistics
""")

st.divider()


tab1, tab2, tab3 = st.tabs(
    [
        "📄 Resume",
        "🤖 AI Analysis",
        "📊 Statistics"
    ]
)


job_role = st.selectbox(
    "Select Target Job Role",
    [
        "Software Engineer",
        "Data Scientist",
        "AI Engineer",
        "Machine Learning Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Cyber Security",
        "Cloud Engineer"
    ]
)

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

resume_text = ""

with tab1:

    if uploaded_file:

        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text.strip():
            st.error("❌ Could not extract text from this PDF.")
            st.stop()

        match_score = calculate_match(resume_text, job_role)

        email = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            resume_text
        )

        phone = re.findall(
            r"\+?\d[\d\s()-]{8,}",
            resume_text
        )

        st.subheader("📇 Contact Information")

        c1, c2 = st.columns(2)

        with c1:
            st.write("📧 Email")
            st.success(email[0] if email else "Not Found")

        with c2:
            st.write("📞 Phone")
            st.success(phone[0] if phone else "Not Found")

        with st.expander("📄 Resume Preview"):
            st.write(resume_text[:3000])

        st.subheader("📈 Resume Match")

        st.progress(match_score)

        st.metric(
            "Keyword Match",
            f"{match_score}%"
        )

        experience = re.findall(
            r"\d+\+?\s+years?",
            resume_text.lower()
        )

        st.subheader("💼 Experience")

        if experience:
            st.success(", ".join(experience))
        else:
            st.info("Experience not detected")

        degrees = [
            "b.tech",
            "b.e",
            "bachelor",
            "m.tech",
            "master",
            "bsc",
            "msc",
            "phd"
        ]

        education = [
            degree
            for degree in degrees
            if degree in resume_text.lower()
        ]

        st.subheader("🎓 Education")

        if education:
            st.success(", ".join(education))
        else:
            st.info("Education not detected")

        sections = [
            "education",
            "experience",
            "projects",
            "skills",
            "certifications",
            "internship"
        ]

        present = sum(
            section in resume_text.lower()
            for section in sections
        )

        completeness = int(
            present / len(sections) * 100
        )

        st.subheader("📋 Resume Completeness")

        st.progress(completeness)

        st.metric(
            "Completeness",
            f"{completeness}%"
        )

        tech_stack = {

            "Programming": [
                "Python",
                "Java",
                "C++",
                "C",
                "JavaScript"
            ],

            "Web": [
                "HTML",
                "CSS",
                "React",
                "Bootstrap",
                "Flask",
                "Django"
            ],

            "Database": [
                "SQL",
                "MySQL",
                "MongoDB"
            ],

            "AI / ML": [
                "TensorFlow",
                "PyTorch",
                "Scikit",
                "Pandas",
                "NumPy"
            ],

            "Cloud": [
                "AWS",
                "Azure",
                "Docker",
                "Kubernetes"
            ]
        }

        st.subheader("🛠 Technologies Found")

        found_any = False

        for category, skills in tech_stack.items():

            found = [
                skill
                for skill in skills
                if skill.lower() in resume_text.lower()
            ]

            if found:
                found_any = True
                st.success(
                    f"**{category}** : {', '.join(found)}"
                )

        if not found_any:
            st.warning("No common technologies detected.")

        words = len(resume_text.split())
        characters = len(resume_text)
        lines = len(resume_text.splitlines())

        st.subheader("📊 Resume Statistics")

        s1, s2, s3 = st.columns(3)

        with s1:
            st.metric("Words", words)

        with s2:
            st.metric("Characters", characters)

        with s3:
            st.metric("Lines", lines)

    else:
        st.info("📄 Upload a resume to begin analysis.")

with tab2:

    if uploaded_file:

        if st.button("🚀 Analyze Resume", use_container_width=True):

            with st.spinner("Analyzing Resume..."):

                try:
                    analysis = analyze_resume(
                        resume_text,
                        job_role
                    )

                except Exception as e:
                    st.error(f"❌ {e}")
                    st.stop()

            st.success("✅ Analysis Completed!")

            match = re.search(
                r"ATS Score:\s*(\d+)",
                analysis,
                re.IGNORECASE
            )

            if match:

                ats_score = int(match.group(1))

                st.subheader("🎯 ATS Score")

                st.progress(ats_score)

                st.metric(
                    "Resume Score",
                    f"{ats_score}/100"
                )

            else:

                st.info(
                    "ATS score not found in AI response."
                )

            st.markdown("---")

            st.subheader("🤖 AI Analysis")

            st.markdown(analysis)

            st.download_button(

                label="📥 Download Analysis",

                data=analysis,

                file_name="resume_analysis.txt",

                mime="text/plain",

                use_container_width=True
            )

    else:

        st.info("Upload a resume first.")

with tab3:

    if uploaded_file:

        st.header("📊 Resume Dashboard")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Keyword Match",
                f"{match_score}%"
            )

            st.metric(
                "Resume Completeness",
                f"{completeness}%"
            )

        with col2:

            st.metric(
                "Words",
                words
            )

            st.metric(
                "Characters",
                characters
            )

        st.divider()

        st.subheader("📈 Overall Summary")

        if completeness >= 80 and match_score >= 80:

            st.success(
                "Excellent resume! Your resume is well-structured and matches the selected role."
            )

        elif completeness >= 60 and match_score >= 60:

            st.warning(
                "Good resume, but adding more relevant skills and improving formatting can increase your ATS score."
            )

        else:

            st.error(
                "Your resume needs significant improvements. Consider adding missing skills, projects, and relevant experience."
            )

    else:

        st.info("Upload a resume to view statistics.")

st.divider()

st.caption(
    "🚀 Built with Python • Streamlit • Groq • Llama 3.3 • PyPDF2"
)