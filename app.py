import re
import streamlit as st
from resume_parser import extract_text_from_pdf
from gemini_analyzer import analyze_resume
from styles import inject_styles        


def calculate_match(resume_text: str, job_role: str) -> int:
    resume = resume_text.lower()
    skills = {
        "Software Engineer":        ["python", "java", "c++", "sql", "git", "oop"],
        "Data Scientist":           ["python", "pandas", "numpy", "machine learning", "sql", "statistics"],
        "AI Engineer":              ["python", "tensorflow", "pytorch", "llm", "transformers", "huggingface"],
        "Machine Learning Engineer":["python", "scikit", "tensorflow", "pytorch", "ml"],
        "Frontend Developer":       ["html", "css", "javascript", "react", "bootstrap"],
        "Backend Developer":        ["python", "django", "flask", "api", "sql"],
        "Cyber Security":           ["network", "linux", "wireshark", "nmap", "security"],
        "Cloud Engineer":           ["aws", "azure", "docker", "kubernetes", "linux"],
    }
    required = skills.get(job_role, [])
    if not required:
        return 0
    found = sum(skill in resume for skill in required)
    return int(found / len(required) * 100)


def score_color(score: int) -> str:
    if score >= 80:
        return "#22c55e"
    if score >= 60:
        return "#f59e0b"
    return "#ef4444"


def render_chip(label: str) -> str:
    return f'<span class="tech-chip">{label}</span>'


# ─────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()   # inject all custom CSS


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown('<p class="eyebrow">Resume Analyzer</p>', unsafe_allow_html=True)
    st.markdown("## 📄 AI Resume Analyzer")
    st.markdown(
        """
        Upload your résumé and get instant, AI-powered feedback on ATS
        compatibility, skill gaps, and actionable improvements.
        """
    )
    st.divider()

    st.markdown('<p class="eyebrow">What you get</p>', unsafe_allow_html=True)
    for feature in [
        "🎯 ATS Compatibility Score",
        "📊 Keyword Match %",
        "🛠 Detected Technologies",
        "💡 AI Suggestions",
        "📋 Resume Completeness",
    ]:
        st.markdown(f"- {feature}")

    st.divider()

    st.markdown('<p class="eyebrow">Stack</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Model", "Llama 3.3")
    with col_b:
        st.metric("Framework", "Streamlit")

    st.markdown("")
    st.caption("Built with Python · Streamlit · Groq · Llama 3.3 · PyPDF2")


# ─────────────────────────────────────────────
#  Hero Header
# ─────────────────────────────────────────────

st.markdown(
    """
    <p class="eyebrow" style="margin-top:0.5rem;">Powered by Llama 3.3 via Groq</p>
    <h1>AI Resume Analyzer</h1>
    <p style="font-size:1.05rem;color:#64748b;max-width:580px;margin-bottom:1.5rem;">
      Get a detailed breakdown of your résumé's ATS score, skill gaps,
      and actionable suggestions — in seconds.
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()


# ─────────────────────────────────────────────
#  Upload + Role Selection  (above the tabs)
# ─────────────────────────────────────────────

col_role, col_upload = st.columns([1, 2], gap="large")

with col_role:
    st.markdown('<p class="eyebrow">Target Role</p>', unsafe_allow_html=True)
    job_role = st.selectbox(
        "Select Target Job Role",
        [
            "Software Engineer", "Data Scientist", "AI Engineer",
            "Machine Learning Engineer", "Frontend Developer",
            "Backend Developer", "Cyber Security", "Cloud Engineer",
        ],
        label_visibility="collapsed",
    )

with col_upload:
    st.markdown('<p class="eyebrow">Your Résumé</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload your résumé (PDF)",
        type=["pdf"],
        label_visibility="collapsed",
    )

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Tabs

tab1, tab2, tab3 = st.tabs(["📄  Overview", "🤖  AI Analysis", "📊  Dashboard"])

resume_text = ""
match_score = completeness = words = characters = lines = 0   # safe defaults

# ── Tab 1 : Overview ──────────────────────────

with tab1:
    if not uploaded_file:
        st.markdown(
            """
            <div class="resume-card" style="text-align:center;padding:3rem 2rem;">
              <p style="font-size:2.5rem;margin-bottom:0.5rem;">📂</p>
              <p style="font-size:1.1rem;color:#64748b;">
                Upload a PDF résumé above to begin your analysis.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        resume_text = extract_text_from_pdf(uploaded_file)

        if not resume_text.strip():
            st.error("❌ Could not extract text from this PDF. Please try a text-based PDF.")
            st.stop()

        match_score  = calculate_match(resume_text, job_role)
        email        = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text)
        phone        = re.findall(r"\+?\d[\d\s()-]{8,}", resume_text)
        experience   = re.findall(r"\d+\+?\s+years?", resume_text.lower())
        degrees      = ["b.tech","b.e","bachelor","m.tech","master","bsc","msc","phd"]
        education    = [d for d in degrees if d in resume_text.lower()]
        sections     = ["education","experience","projects","skills","certifications","internship"]
        present      = sum(s in resume_text.lower() for s in sections)
        completeness = int(present / len(sections) * 100)
        words        = len(resume_text.split())
        characters   = len(resume_text)
        lines        = len(resume_text.splitlines())

        # ── Contact ──
        st.markdown('<p class="eyebrow">Contact Information</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.markdown(
                f"""
                <div class="resume-card">
                  <p style="color:#64748b;font-size:0.75rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.3rem;">EMAIL</p>
                  <p style="font-size:1rem;color:#e2e8f0;font-weight:500;">{email[0] if email else "—"}</p>
                </div>
                """, unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f"""
                <div class="resume-card">
                  <p style="color:#64748b;font-size:0.75rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.3rem;">PHONE</p>
                  <p style="font-size:1rem;color:#e2e8f0;font-weight:500;">{phone[0].strip() if phone else "—"}</p>
                </div>
                """, unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Scores row ──
        st.markdown('<p class="eyebrow">Resume Scores</p>', unsafe_allow_html=True)
        s1, s2 = st.columns(2, gap="medium")
        with s1:
            st.markdown(
                f"""
                <div class="resume-card">
                  <p style="color:#64748b;font-size:0.75rem;letter-spacing:.08em;text-transform:uppercase;">KEYWORD MATCH — {job_role}</p>
                  <p style="font-size:2.2rem;font-weight:700;color:{score_color(match_score)};margin:.25rem 0;">{match_score}<span style="font-size:1.1rem;color:#64748b;">%</span></p>
                </div>
                """, unsafe_allow_html=True
            )
            st.progress(match_score / 100)
        with s2:
            st.markdown(
                f"""
                <div class="resume-card">
                  <p style="color:#64748b;font-size:0.75rem;letter-spacing:.08em;text-transform:uppercase;">COMPLETENESS</p>
                  <p style="font-size:2.2rem;font-weight:700;color:{score_color(completeness)};margin:.25rem 0;">{completeness}<span style="font-size:1.1rem;color:#64748b;">%</span></p>
                </div>
                """, unsafe_allow_html=True
            )
            st.progress(completeness / 100)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Experience & Education ──
        e1, e2 = st.columns(2, gap="medium")
        with e1:
            st.markdown('<p class="eyebrow">Experience Detected</p>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="resume-card">
                  <p style="color:#e2e8f0;font-size:1rem;">{", ".join(experience) if experience else "No explicit experience duration found."}</p>
                </div>
                """, unsafe_allow_html=True
            )
        with e2:
            st.markdown('<p class="eyebrow">Education Detected</p>', unsafe_allow_html=True)
            chips = " ".join(render_chip(d.upper()) for d in education) if education else '<span style="color:#64748b;">Not detected</span>'
            st.markdown(
                f'<div class="resume-card">{chips}</div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Technologies ──
        st.markdown('<p class="eyebrow">Technologies Detected</p>', unsafe_allow_html=True)
        tech_stack = {
            "Programming": ["Python","Java","C++","C","JavaScript"],
            "Web":         ["HTML","CSS","React","Bootstrap","Flask","Django"],
            "Database":    ["SQL","MySQL","MongoDB"],
            "AI / ML":     ["TensorFlow","PyTorch","Scikit","Pandas","NumPy"],
            "Cloud":       ["AWS","Azure","Docker","Kubernetes"],
        }
        all_found: dict[str, list[str]] = {}
        for cat, items in tech_stack.items():
            found = [s for s in items if s.lower() in resume_text.lower()]
            if found:
                all_found[cat] = found

        if all_found:
            html_block = '<div class="resume-card">'
            for cat, found in all_found.items():
                html_block += f'<p style="color:#64748b;font-size:0.7rem;letter-spacing:.08em;text-transform:uppercase;margin:0.75rem 0 0.3rem;">{cat}</p>'
                html_block += "".join(render_chip(s) for s in found)
            html_block += "</div>"
            st.markdown(html_block, unsafe_allow_html=True)
        else:
            st.warning("No common technologies detected in the résumé.")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Resume Preview ──
        with st.expander("📄 Preview extracted text"):
            st.code(resume_text[:3000], language=None)

# ── Tab 2 : AI Analysis ───────────────────────

with tab2:
    if not uploaded_file:
        st.info("Upload a résumé first to run the AI analysis.")
    else:
        if st.button("🚀 Run AI Analysis", use_container_width=True):
            with st.spinner("Analyzing your résumé with Llama 3.3…"):
                try:
                    analysis = analyze_resume(resume_text, job_role)
                except Exception as e:
                    st.error(f"❌ {e}")
                    st.stop()

            st.success("✅ Analysis complete!")

            ats_match = re.search(r"ATS Score:\s*(\d+)", analysis, re.IGNORECASE)
            if ats_match:
                ats_score = int(ats_match.group(1))
                st.markdown('<p class="eyebrow" style="margin-top:1rem;">ATS Score</p>', unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div class="resume-card" style="display:flex;align-items:center;gap:2rem;">
                      <p style="font-size:3rem;font-weight:700;color:{score_color(ats_score)};margin:0;">{ats_score}<span style="font-size:1.2rem;color:#64748b;">/100</span></p>
                      <p style="color:#94a3b8;margin:0;font-size:0.95rem;">
                        {"Strong ATS match — your résumé is well-optimised." if ats_score >= 80
                         else "Moderate match — a few tweaks can boost your score." if ats_score >= 60
                         else "Needs work — consider the AI suggestions below."}
                      </p>
                    </div>
                    """, unsafe_allow_html=True
                )
                st.progress(ats_score / 100)
            else:
                st.info("ATS score not present in the AI response — see the full analysis below.")

            st.divider()

            st.markdown('<p class="eyebrow">Full AI Feedback</p>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="resume-card" style="line-height:1.8;">{analysis}</div>',
                unsafe_allow_html=True,
            )

            st.download_button(
                label="📥 Download Analysis",
                data=analysis,
                file_name="resume_analysis.txt",
                mime="text/plain",
                use_container_width=True,
            )

# ── Tab 3 : Dashboard ─────────────────────────

with tab3:
    if not uploaded_file:
        st.info("Upload a résumé to view the dashboard.")
    else:
        st.markdown('<p class="eyebrow">Resume Dashboard</p>', unsafe_allow_html=True)

        d1, d2, d3, d4 = st.columns(4, gap="medium")
        for col, label, value in [
            (d1, "Keyword Match", f"{match_score}%"),
            (d2, "Completeness",  f"{completeness}%"),
            (d3, "Word Count",    str(words)),
            (d4, "Characters",    str(characters)),
        ]:
            with col:
                st.metric(label, value)

        st.divider()

        # Score bars
        st.markdown('<p class="eyebrow">Score Breakdown</p>', unsafe_allow_html=True)
        bar_data = {
            "Keyword Match":   match_score,
            "Completeness":    completeness,
        }
        for label, val in bar_data.items():
            c_label, c_bar = st.columns([1, 4], gap="small")
            with c_label:
                st.markdown(
                    f'<p style="color:#94a3b8;font-size:0.85rem;padding-top:4px;">{label}</p>',
                    unsafe_allow_html=True,
                )
            with c_bar:
                st.progress(val / 100)
                st.caption(f"{val}%")

        st.divider()

        # Summary verdict
        st.markdown('<p class="eyebrow">Verdict</p>', unsafe_allow_html=True)
        if completeness >= 80 and match_score >= 80:
            st.success(
                "✅ **Excellent résumé.** Well-structured and closely matched to the selected role. "
                "Submit with confidence."
            )
        elif completeness >= 60 and match_score >= 60:
            st.warning(
                "⚡ **Good résumé.** Adding a few more role-specific keywords and rounding out "
                "any missing sections will push your ATS score higher."
            )
        else:
            st.error(
                "🔧 **Needs improvement.** Consider expanding the skills, projects, and experience "
                "sections with keywords relevant to the target role."
            )


#  Footer

st.divider()
st.caption("📄 AI Resume Analyzer · Built with Python · Streamlit · Groq · Llama 3.3 · PyPDF2")
