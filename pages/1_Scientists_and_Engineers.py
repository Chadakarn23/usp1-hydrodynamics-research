import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
from data import IMG, FLOW_RATE_DATA, sidebar_about

st.set_page_config(page_title="For Scientists & Engineers", page_icon="💊", layout="wide")
sidebar_about()

st.header("💊 Why Hydrodynamics Matters for Dissolution Testing")
st.markdown("""
**For formulation scientists, analytical chemists, CMC/regulatory professionals, 
and CFD engineers** working with USP dissolution testing systems.

Most scientists treat the dissolution apparatus as a black box — 
you drop a tablet in and get a number out. **This tool opens that black box** 
and shows you *why* you get the number you do.
""")

st.markdown("---")

st.markdown("### 🎯 5 Things Every Formulation Scientist Should Know")

st.markdown("#### 1️⃣ Basket Mesh Selection Changes the Flow by 70%")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    The mesh isn't just about retaining tablet fragments — it controls how much liquid 
    flows through the basket and around your dosage form:
    
    | Mesh | Wire Opening | Q through basket | Relative Flow |
    |:----:|:-----------:|:----------------:|:-------------:|
    | 10-mesh | 1.90 mm | 7.1 mL/s | **100%** |
    | 20-mesh | 0.86 mm | 6.5 mL/s | 91% |
    | 40-mesh | 0.40 mm | 4.2 mL/s | **59%** |
    
    A tablet inside a 10-mesh basket sees **70% more flow** than in a 40-mesh. 
    This directly affects dissolution rate, especially for BCS Class II compounds.
    
    → *Go to the* ***Flow Rate*** *page to explore this interactively.*
    """)
with col2:
    st.image(str(IMG / "cfd-10mesh-velocity.png"), caption="10-mesh: stronger flow below basket", use_container_width=True)
    st.caption("CFD simulation results from the author's original research.")

st.markdown("---")

st.markdown("#### 2️⃣ OOS Results? Check the Hydrodynamics First")
st.markdown("""
The velocity field below the basket is **highly non-uniform**:
- Strong tangential flow near basket edge, near-zero velocity at center
- A tablet fragment 5 mm off-center sees **completely different shear** than one at center
- USP allows ±2 mm basket positioning tolerance — the flow field changes significantly within that range

**This is a root cause for vessel-to-vessel variability** that your OOS investigation might miss.

→ *Go to the* ***CFD vs PIV*** *page and look at the velocity gradients near r/R = 0.25.*
""")

st.markdown("---")

st.markdown("#### 3️⃣ No Coning in USP-1 (Unlike the Paddle)")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **USP Apparatus 2 (Paddle)** has a well-known problem: tablet granules pile up 
    in a "cone" below the impeller because the central core has near-zero velocity.
    
    **USP Apparatus 1 (Basket)** does NOT have this problem because:
    - Strong upward axial flow through the basket base
    - Fragments that fall out get swept outward by the recirculation loop
    - The central core below the basket has **stronger** flow than USP-2
    
    *Source: CES 2023, Section 5.3*
    """)
with col2:
    st.image(str(IMG / "cfd-20mesh-velocity.png"), caption="Upward flow visible below the basket", use_container_width=True)
    st.caption("CFD simulation results from the author's original research.")

st.markdown("---")

st.markdown("#### 4️⃣ Regulatory Justification With Peer-Reviewed Data")
st.markdown("""
When FDA asks *"Why did you choose this basket mesh and RPM?"*, you can point to:
- ✅ Validated CFD velocity fields showing the hydrodynamic environment
- ✅ Quantified flow rates (Q_in/Q_out) for each mesh size
- ✅ Strain rate and energy dissipation rate distributions
- ✅ **5 peer-reviewed publications** backing every number

→ *Go to the* ***Publications & About*** *page for the full citation list.*
""")

st.markdown("---")

st.markdown("#### 5️⃣ Mixing Time Affects Your Sample Representativeness")
st.markdown("""
If mixing is slow (fine mesh + large volume), concentration gradients persist in the vessel. 
The sample you pull might not represent the bulk dissolved concentration:

- **10-mesh, 500 mL** → fastest mixing → most representative samples
- **40-mesh, 900 mL** → slowest mixing → samples may underestimate true dissolution

→ *Go to the* ***Mixing Time*** *page for details.*
""")

st.markdown("---")
st.markdown("""
### From Static Publications to Interactive Exploration

Scientific publications present results as static figures and tables — useful for
peer review, but limiting for day-to-day engineering decisions. This tool reimagines
that same validated research as an **interactive, queryable resource**.

| | |
|---|---|
| **Research foundation** | 6 peer-reviewed publications (2017–2023), doctoral dissertation, and 5+ years of CFD modeling and PIV experiments on pharmaceutical dissolution systems |
| **Process modeling expertise** | The author defined the physics, curated the validated datasets, designed the analysis framework, and verified every output against published results |
| **Generative AI as an engineering tool** | Large language models were leveraged as coding accelerators — translating the author's technical specifications directly into interactive Streamlit/Plotly code, demonstrating how GenAI can extend an engineer's capability beyond traditional toolsets |

The scientific content — turbulence model selection, mesh independence criteria, 
CFD–PIV validation, flow rates, power numbers, and mixing times — originates entirely 
from the author's published work. The AI contributed to the implementation, not to 
the engineering judgment behind it.

> *Process modeling engineers generate enormous amounts of validated simulation
> data that often remains locked in PDFs and slide decks. Generative AI makes it
> practical to convert that domain knowledge into interactive tools — a new competency
> at the intersection of engineering expertise and AI fluency.*

**Full publication list in the Publications & About page.**
""")
