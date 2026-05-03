"""
Dissolution Apparatus Hydrodynamics Explorer — Landing Page
"""
import streamlit as st
import glob, os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import sidebar_about

st.set_page_config(
    page_title="Dissolution Apparatus Hydrodynamics Explorer",
    page_icon="🌀",
    layout="wide",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Remove default Streamlit top padding */
    .block-container { padding-top: 1rem; }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #0e4c75 0%, #1a7ab5 60%, #3ba3d9 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
        color: white;
    }
    .hero-banner h1 {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
        color: white;
    }
    .hero-banner p {
        font-size: 1.1rem;
        opacity: 0.92;
        max-width: 720px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Stat pills */
    .stat-bar {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1.5rem 0 0.5rem;
    }
    .stat-pill {
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 24px;
        padding: 0.4rem 1.2rem;
        font-size: 0.92rem;
        font-weight: 600;
        color: white;
    }

    /* Section cards (navigation) */
    .nav-card {
        background: white;
        border: 1px solid #e3e8ee;
        border-radius: 12px 12px 0 0;
        padding: 1.5rem 1.2rem 1rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .nav-card .icon { font-size: 2.8rem; margin-bottom: 0.6rem; }
    .nav-card .title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0e4c75;
        margin-bottom: 0.4rem;
    }
    .nav-card .desc {
        font-size: 0.85rem;
        color: #5a6a7a;
        line-height: 1.45;
    }

    /* Clickable card link wrapper */
    a.nav-card-link {
        text-decoration: none;
        display: block;
        border-radius: 12px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    a.nav-card-link:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(14,76,117,0.12);
    }
    a.nav-card-link:hover .nav-card {
        border-color: #1a7ab5;
        background: linear-gradient(135deg, #f0f7fc 0%, #ffffff 100%);
    }
    a.nav-card-link:hover .card-foot {
        border-color: #1a7ab5;
        background: linear-gradient(135deg, #eaf4fb 0%, #ffffff 100%);
        color: #0b3d5e;
    }

    /* Card footer — styled as bottom of card */
    .card-foot {
        border: 1px solid #e3e8ee;
        border-top: none;
        background: white;
        color: #1a7ab5;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0.55rem 0;
        border-radius: 0 0 12px 12px;
        text-align: center;
        transition: background 0.2s ease, border-color 0.2s ease;
    }

    /* Key finding callout */
    .callout {
        background: #f0f7fc;
        border-left: 5px solid #1a7ab5;
        border-radius: 0 10px 10px 0;
        padding: 1.1rem 1.5rem;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .callout strong { color: #0e4c75; }

    /* Who-is-this-for */
    .audience-card {
        background: #fafbfc;
        border: 1px solid #e3e8ee;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        min-height: 100%;
    }
    .audience-card h4 { color: #0e4c75; margin-bottom: 0.3rem; font-size: 1rem; }
    .audience-card p { color: #5a6a7a; font-size: 0.88rem; margin: 0; line-height: 1.5; }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #8a9bb0;
        font-size: 0.82rem;
        padding: 1rem 0 0.5rem;
        border-top: 1px solid #e3e8ee;
    }
</style>
""", unsafe_allow_html=True)

sidebar_about()

# ─── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>🌀 Dissolution Apparatus Hydrodynamics Explorer</h1>
    <p>
        Interactive research tool for exploring validated CFD and PIV data
        in USP Dissolution Apparatus 1 (rotating basket). Built from doctoral
        dissertation research and 5 peer-reviewed publications.
        Now featuring <strong>BCS-guided method development</strong> and a <strong>condition scaling calculator</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Key Finding ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="callout">
    <strong>Key Finding:</strong> Of 4 RANS turbulence models tested, only
    <strong>Realizable k-ε with Standard Wall Functions</strong> achieved both
    convergence (residuals &lt; 10⁻⁴) and agreement with PIV experiments.
    &nbsp;•&nbsp; 100 RPM &nbsp;•&nbsp; 900 mL water at 20 °C &nbsp;•&nbsp; Re ≈ 1075
    &nbsp;•&nbsp; <span style="background:rgba(255,255,255,0.25); border-radius:8px; padding:2px 8px;">🧬 BCS integration + 🔢 Condition Calculator now available</span>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# ─── Navigation Cards ────────────────────────────────────────────────────────
st.markdown("### Explore the Research")

CARDS = [
    ("💊", "Scientists & Engineers", "Practical pharma applications — method development, OOS investigation, regulatory justification"),
    ("📋", "Model Selection", "Compare 4 RANS turbulence models — convergence and PIV agreement"),
    ("🔲", "Mesh Independence", "Why 20-mesh needs 3.5× more cells than 10-mesh"),
    ("📊", "CFD vs PIV", "Validation across 7 measurement planes + flow rate comparison"),
    ("🔄", "Flow Rate", "Volumetric flow through the basket — PIV & CFD predictions"),
    ("⚡", "Power Number", "Power consumption (Po) comparison across basket mesh sizes"),
    ("⏱️", "Mixing Time", "Blend time data across fill volumes and mesh sizes"),
    ("📖", "CFD Knowledge Base", "Setup recipe — turbulence model, mesh, solver, boundary conditions"),
    ("📚", "Publications & About", "Full publication list with DOIs — every data point traced to source"),
    ("🧬", "BCS Method Development", "NEW — BCS class wizard, sensitivity heatmap, OOS guide, regulatory context"),
    ("🔢", "Condition Calculator", "NEW — Scale RPM, temperature & volume; estimate Re, flow rate, blend time"),
]

# Build page URL lookup from actual files on disk
_app_dir = os.path.dirname(os.path.abspath(__file__))
_page_files = sorted(glob.glob(os.path.join(_app_dir, "pages", "*.py")))
_url_map = {}
for f in _page_files:
    name = os.path.basename(f)
    num = name.split("_")[0]
    # Streamlit strips the leading number + underscore for the URL path
    slug = os.path.splitext(name)[0]                        # "1_Scientists_and_Engineers"
    slug = "_".join(slug.split("_")[1:])                    # "Scientists_and_Engineers"
    _url_map[int(num)] = "/" + slug

for row_start in range(0, len(CARDS), 3):
    cards_html = '<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:1rem; margin-bottom:1rem;">'
    for i in range(3):
        idx = row_start + i
        if idx < len(CARDS) and idx < 11:
            icon, title, desc = CARDS[idx]
            page_num = idx + 1
            href = _url_map.get(page_num, "#")
            cards_html += f'''
            <a class="nav-card-link" href="{href}" target="_blank" rel="noopener">
                <div class="nav-card">
                    <div class="icon">{icon}</div>
                    <div class="title">{title}</div>
                    <div class="desc">{desc}</div>
                </div>
                <div class="card-foot">Explore →</div>
            </a>'''
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

st.markdown("---")

# ─── Who Is This For ──────────────────────────────────────────────────────────
st.markdown("### Who Is This For?")
audience = [
    ("🧪", "Formulation Scientists", "Understand how basket mesh size affects flow around your dosage form"),
    ("🔬", "Analytical R&D", "Justify dissolution method parameters with validated hydrodynamic data"),
    ("📝", "CMC / Regulatory", "Answer FDA questions with peer-reviewed CFD evidence"),
    ("💻", "CFD Engineers", "Get validated settings as a starting point for your simulations"),
    ("🎓", "Students & Researchers", "Benchmark your USP-1 simulations against published experimental data"),
    ("⚙️", "Process Engineers", "Understand dissolution variability through hydrodynamic analysis"),
]

for row_start in range(0, 6, 3):
    cols = st.columns(3, gap="medium")
    for i, col in enumerate(cols):
        idx = row_start + i
        if idx < len(audience):
            a_icon, a_title, a_desc = audience[idx]
            with col:
                st.markdown(f"""
                <div class="audience-card">
                    <h4>{a_icon} {a_title}</h4>
                    <p>{a_desc}</p>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-text">
    <strong>Dissolution Apparatus Hydrodynamics Explorer</strong> 
    &nbsp;|&nbsp; Built with Streamlit + Plotly &nbsp;|&nbsp; AI-accelerated development<br>
    Data from 5 peer-reviewed publications & doctoral dissertation<br>
    © 2026 Chadakarn Sirasitthichoke &nbsp;|&nbsp; 
    Engineering expertise + Generative AI = interactive research tools
</div>
""", unsafe_allow_html=True)
