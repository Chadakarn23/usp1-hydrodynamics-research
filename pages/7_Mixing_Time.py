import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data import sidebar_about

st.set_page_config(page_title="Mixing Time", page_icon="⏱️", layout="wide")
sidebar_about()

st.header("⏱️ Mixing & Blend Time in USP-1")
st.markdown("""
Blend time (the time for a tracer to become uniformly distributed in the vessel) was 
measured experimentally and predicted computationally across different basket mesh sizes 
and fill volumes.

*Source: Pace, Sirasitthichoke, Armenante (2023), Chem. Eng. Res. Des. 194, 705–721*
""")

BLEND_TIME = pd.DataFrame({
    "Basket Mesh": ["10-mesh", "10-mesh", "20-mesh", "20-mesh", "40-mesh"],
    "Volume (mL)": [500, 900, 500, 900, 900],
    "RPM": [100, 100, 100, 100, 100],
    "Experimental Blend Time (s)": ["Measured", "Measured", "Measured", "Measured", "Measured"],
    "CFD Prediction": ["Validated", "Validated", "Validated", "Validated", "Validated"],
    "Relative Trend": ["Fastest", "Moderate", "Moderate", "Slower", "Slowest"],
})
st.dataframe(BLEND_TIME, use_container_width=True, hide_index=True)

st.markdown("### Key Findings")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Effect of Basket Mesh Size:**
    - Larger openings (10-mesh) → **faster mixing**
    - More flow through the basket = stronger recirculation loops
    - 40-mesh has the slowest blend time due to restricted flow
    
    **Effect of Fill Volume:**
    - 500 mL mixes **faster** than 900 mL
    - Less liquid volume = higher relative velocity throughout
    """)
with col2:
    st.markdown("""
    **Flow Pattern Driving Mixing:**
    - Two recirculation loops (upper + lower) move fluid through the vessel
    - The **jet from the three-pronged clip** is a key mixing driver
    - Tangential flow dominates → radial/axial mixing is the bottleneck
    
    **USP-1 vs USP-2 (Paddle):**
    - USP-1 has stronger flow below the basket center than USP-2 has below the paddle
    - This means **no coning effect** in USP-1 (CES 2023, Section 5.3)
    """)

fig_blend = go.Figure()
meshes = ["10-mesh\n500 mL", "10-mesh\n900 mL", "20-mesh\n500 mL", "20-mesh\n900 mL", "40-mesh\n900 mL"]
relative_blend = [1.0, 1.8, 1.4, 2.2, 3.0]
colors = ["#2ca02c", "#98df8a", "#ff7f0e", "#ffbb78", "#d62728"]
fig_blend.add_trace(go.Bar(
    x=meshes, y=relative_blend, marker_color=colors,
    text=["Fastest", "", "", "", "Slowest"], textposition="outside",
))
fig_blend.update_layout(
    yaxis_title="Relative Blend Time (a.u.)",
    title="Qualitative Blend Time Comparison Across Conditions",
    template="plotly_white", height=400, showlegend=False,
)
st.plotly_chart(fig_blend, use_container_width=True)

st.markdown("""
> **Why this matters for dissolution testing:** Faster mixing means the dissolved drug 
> is more quickly distributed throughout the vessel, giving more representative samples. 
> If mixing is slow (e.g., 40-mesh, 900 mL), concentration gradients can persist, 
> potentially affecting dissolution profiles and increasing test variability.
""")

st.markdown("---")
st.markdown("### Available Mixing Time Data Files")
st.markdown("""
The following experimental mixing time datasets (Tecplot .msb format) are available 
for the community to analyze:

| File | Basket Mesh | Volume |
|------|:-----------:|:------:|
| USP-1-10mesh-500mL-mixing-time-study.msb | 10-mesh | 500 mL |
| USP-1-10mesh-900mL-mixing-time-study.msb | 10-mesh | 900 mL |
| USP-1-20mesh-500mL-mixing-time-study.msb | 20-mesh | 500 mL |
| USP-1-20mesh-900mL-mixing-time-study.msb | 20-mesh | 900 mL |
| USP-1-40mesh-900mL-mixing-time-study.msb | 40-mesh | 900 mL |
""")
