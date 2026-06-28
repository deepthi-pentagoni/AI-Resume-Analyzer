"""
styles.py  –  drop this file next to app.py and call inject_styles() once.
"""

def inject_styles():
    import streamlit as st

    st.markdown("""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;700&display=swap');

    /* ── Base Reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── App Background ── */
    .stApp {
        background: #0a0e1a;
        color: #e2e8f0;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #0f1527 !important;
        border-right: 1px solid #1e2a45;
    }
    section[data-testid="stSidebar"] * {
        color: #a0aec0 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #e2e8f0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    section[data-testid="stSidebar"] .stMetric label {
        color: #64748b !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    section[data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: #7c3aed !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .stDivider {
        border-color: #1e2a45 !important;
    }

    /* ── Main Title & Hero ── */
    h1 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2.6rem !important;
        background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #38bdf8 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        letter-spacing: -0.02em;
    }
    h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #e2e8f0 !important;
    }
    p, li {
        color: #94a3b8;
        line-height: 1.7;
    }

    /* ── Cards / Custom Containers ── */
    .resume-card {
        background: #111827;
        border: 1px solid #1e2a45;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }

    /* ── Metric Overrides ── */
    [data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #1e2a45;
        border-radius: 10px;
        padding: 1rem 1.25rem;
    }
    [data-testid="stMetric"] label {
        color: #64748b !important;
        font-size: 0.7rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        color: #818cf8 !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    /* ── Progress Bar ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #a78bfa) !important;
        border-radius: 99px !important;
    }
    .stProgress > div {
        background: #1e2a45 !important;
        border-radius: 99px !important;
        height: 8px !important;
    }

    /* ── File Uploader ── */
    [data-testid="stFileUploader"] {
        background: #111827 !important;
        border: 2px dashed #2d3f63 !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        transition: border-color 0.2s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1 !important;
    }
    [data-testid="stFileUploader"] label {
        color: #94a3b8 !important;
    }

    /* ── Selectbox ── */
    [data-testid="stSelectbox"] > div > div {
        background: #111827 !important;
        border: 1px solid #2d3f63 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #111827;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #1e2a45;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #64748b !important;
        border-radius: 8px !important;
        font-weight: 500;
        padding: 0.5rem 1.25rem;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: #6366f1 !important;
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1.5rem;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.6rem 1.5rem !important;
        transition: opacity 0.2s, transform 0.1s !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.35) !important;
        letter-spacing: 0.01em;
    }
    .stButton > button:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }
    .stDownloadButton > button {
        background: #0f172a !important;
        border: 1px solid #6366f1 !important;
        color: #818cf8 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }

    /* ── Alert / Info / Success / Warning / Error boxes ── */
    .stAlert {
        border-radius: 8px !important;
        border-width: 1px !important;
    }
    [data-testid="stAlert"] [kind="info"] {
        background: #0f1f3d !important;
        border-color: #1e40af !important;
    }
    .stSuccess {
        background: #052e16 !important;
        border-color: #166534 !important;
        color: #86efac !important;
    }
    .stWarning {
        background: #1c1003 !important;
        border-color: #854d0e !important;
        color: #fde68a !important;
    }
    .stError {
        background: #1c0404 !important;
        border-color: #991b1b !important;
        color: #fca5a5 !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: #111827 !important;
        border: 1px solid #1e2a45 !important;
        border-radius: 10px !important;
    }
    [data-testid="stExpander"] summary {
        color: #94a3b8 !important;
        font-weight: 500;
    }

    /* ── Divider ── */
    hr {
        border-color: #1e2a45 !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Caption / Footer ── */
    .stCaption, footer {
        color: #334155 !important;
        font-size: 0.75rem;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0e1a; }
    ::-webkit-scrollbar-thumb { background: #2d3f63; border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: #6366f1; }

    /* ── Tag chips for technologies ── */
    .tech-chip {
        display: inline-block;
        background: #1e1b4b;
        color: #a5b4fc;
        border: 1px solid #3730a3;
        border-radius: 999px;
        padding: 2px 12px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 3px 3px 3px 0;
    }

    /* ── Section label eyebrow ── */
    .eyebrow {
        font-size: 0.68rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6366f1;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)