import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from data import PUBLICATIONS, sidebar_about

st.set_page_config(page_title="Publications & About", page_icon="📚", layout="wide")
sidebar_about()

st.header("📚 Publications & About This Project")

st.markdown("""
### The Research Behind This Tool

This interactive explorer is built on data from **5 peer-reviewed publications** 
and a doctoral dissertation, spanning experimental (PIV) and computational (CFD) 
approaches to characterize hydrodynamics in pharmaceutical dissolution 
testing and stirred vessel systems.

The original research was conducted as part of a 5-year PhD program. Today, generative 
AI makes it possible to transform that body of work into a tool that others can explore 
and build upon — extending the impact of the research beyond static publications.
""")

st.markdown("---")
st.markdown("### 📄 Peer-Reviewed Publications")

for p in PUBLICATIONS:
    with st.expander(f"**[{p['year']}]** {p['title']}"):
        st.markdown(f"**Authors:** {p['authors']}")
        st.markdown(f"**Journal:** {p['journal']}")
        if p["doi"]:
            st.markdown(f"**DOI:** [{p['doi']}](https://doi.org/{p['doi']})")
        st.markdown(f"**Topics:** {', '.join(p['topics'])}")
        st.markdown(f"**Data used in tabs:** {p['tabs']}")

st.markdown("---")
st.markdown("### From Research to Interactive Tool")
st.markdown("""
This app was built by combining process modeling expertise with generative AI:

1. **Domain knowledge drives every decision** — Selecting the correct turbulence model,
   validating CFD against PIV experiments, and interpreting flow physics all required
   years of research experience. No AI model can substitute for that judgment.
2. **Generative AI accelerates the translation** — LLMs were used as coding accelerators
   to convert the author's technical specifications into interactive Streamlit/Plotly code,
   bridging the gap between validated research and shareable tooling.
3. **Open-source enables community building** — Fork this repo, add your own dissolution
   data, and contribute back.

**Stack:** Python + Streamlit + Plotly + NumPy/Pandas  
**License:** MIT — use it, modify it, share it.
""")

st.markdown("---")
st.markdown("### 🔗 How to Cite")
st.markdown("""
If you use this tool or the underlying data, please cite the relevant publication(s) above.  
For the CFD model selection and PIV validation data shown in this app, the primary reference is:
""")
st.code("""
Sirasitthichoke, C., Patel, S., Reuter, K., Hermans, A., Bredael, G., Armenante, P.M. (2023).
Computational Determination of Hydrodynamics in the USP Dissolution Testing Apparatus 1.
Chemical Engineering Science, 280, 118946.
DOI: 10.1016/j.ces.2023.118946
""", language=None)
st.markdown("For PIV experimental data:")
st.code("""
Sirasitthichoke, C., Perivilli, S., Liddell, M.R., Armenante, P.M. (2021).
Experimental Determination of the Velocity Distribution in USP Apparatus 1
Using Particle Image Velocimetry (PIV).
International Journal of Pharmaceutics: X, 3, 100078.
""", language=None)

st.markdown("---")
st.markdown("### 👤 About the Author")
st.markdown("""
**Chadakarn Sirasitthichoke, PhD**  
MS&T Systems & Engineering | Bristol Myers Squibb  
PhD in Chemical Engineering, NJIT (2021)  

Research interests: CFD, mixing, dissolution testing, process scale-up, 
multivariate data analysis, AI/ML for pharmaceutical engineering
""")
