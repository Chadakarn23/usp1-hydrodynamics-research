import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import plotly.graph_objects as go
from data import MODEL_SELECTION, IMG, sidebar_about

st.set_page_config(page_title="Model Selection", page_icon="📋", layout="wide")
sidebar_about()

st.header("📋 Turbulence Model Selection")
st.markdown("""
Four RANS turbulence models were tested for the USP-1 basket apparatus at 100 RPM, 900 mL.  
The key criteria were: (1) convergence of scaled residuals below 10⁻⁴, and 
(2) agreement with PIV measurements from [Sirasitthichoke et al., 2021a].

*Source: Sirasitthichoke et al. (2023), Chemical Engineering Science, 280, 118946 — Section 3.3, Fig. 5*
""")

st.dataframe(
    MODEL_SELECTION.style.map(
        lambda v: "background-color: #d4edda" if v == "✓" else 
                  ("background-color: #f8d7da" if v == "✗" else ""),
        subset=["PIV Agreement"]
    ),
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Key Finding")
    st.info("""
    **Realizable k-ε with Standard Wall Functions** was the only model that achieved 
    both convergence (residuals < 10⁻⁴) and good agreement with PIV data.
    
    - y⁺ < 5 maintained at all solid surfaces
    - ~12,000 iterations to convergence
    - Monitored via volume-averaged tangential velocity
    - Three-pronged clip included in geometry (critical for jet prediction)
    """)

with col2:
    st.markdown("### Why Other Models Failed")
    st.warning("""
    **k-ω (Low Re):** Comparison with previous experimental PIV data 
    "was not favorable" (CES 2023, Section 2). No longer considered.
    
    **Standard k-ε + Enhanced Wall:** Failed to converge to residuals < 10⁻⁴.
    Over-predicted near-wall turbulence in the basket region.
    
    **Realizable k-ε + Enhanced Wall:** Failed to converge similarly.
    Standard Wall Functions outperformed Enhanced Wall Treatment for this geometry.
    """)

# Convergence chart
st.markdown("### Convergence Behavior")
fig_conv = go.Figure()
models = MODEL_SELECTION["Turbulence Model"] + " + " + MODEL_SELECTION["Wall Treatment"]
colors = ["#dc3545", "#dc3545", "#dc3545", "#28a745"]
fig_conv.add_trace(go.Bar(
    x=models, y=[5e-2, 1e-2, 5e-3, 8e-5],
    marker_color=colors,
    text=MODEL_SELECTION["Residual Convergence"],
    textposition="outside",
))
fig_conv.add_hline(y=1e-4, line_dash="dash", line_color="blue",
                   annotation_text="Target: 10⁻⁴")
fig_conv.update_layout(
    yaxis_title="Final Residual Level", yaxis_type="log",
    template="plotly_white", height=400, showlegend=False,
)
st.plotly_chart(fig_conv, use_container_width=True)

# CFD contour images
st.markdown("### CFD Velocity Contours — Selected Model vs Failed Model")
st.markdown("*Actual CFD results from the Realizable k-ε (selected) vs k-ω (failed) simulations.*")
col_img1, col_img2 = st.columns(2)
with col_img1:
    _img = IMG / "cfd-selected-model.png"
    if _img.exists():
        st.image(str(_img), caption="✅ Realizable k-ε + Std Wall Functions (selected)", use_container_width=True)
        st.caption("CFD simulation results from the author's original research.")
with col_img2:
    _img = IMG / "cfd-kw-failed.png"
    if _img.exists():
        st.image(str(_img), caption="❌ k-ω Low Re (failed — noisy, non-physical)", use_container_width=True)
        st.caption("CFD simulation results from the author's original research.")
