import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from data import MESH_INDEP, FINAL_MESHES, sidebar_about

st.set_page_config(page_title="Mesh Independence", page_icon="🔲", layout="wide")
sidebar_about()

st.header("🔲 Mesh Independence Study")
st.markdown("""
Grid independence was verified by monitoring **turbulent energy dissipation rate (ε)** and 
**turbulent kinetic energy (k)** as a function of number of cells (CES 2023, Fig. 4). 
For the 10-mesh basket, independence was achieved above **~1.4 million cells**.

Two final meshes were selected: 10-mesh (2.15M) and 20-mesh (7.49M elements).

*Source: Sirasitthichoke et al. (2023), CES 280, Section 3.2, Fig. 4*
""")

fig_mesh = make_subplots(specs=[[{"secondary_y": True}]])
mesh_data = MESH_INDEP[MESH_INDEP["Converged"]].sort_values("Elements")
fig_mesh.add_trace(go.Scatter(
    x=mesh_data["Elements"] / 1e6,
    y=mesh_data["Tangential Velocity (m/s)"].abs(),
    mode="markers+lines", name="Volume-Avg |V_tangential|",
    marker=dict(size=10, color="blue"), line=dict(color="blue", width=2),
))
for _, row in FINAL_MESHES.iterrows():
    fig_mesh.add_trace(go.Scatter(
        x=[row["Elements"] / 1e6],
        y=[abs(row["Tangential Velocity (m/s)"])],
        mode="markers", name=f"Selected: {int(row['Basket Mesh Size'])}-mesh",
        marker=dict(size=16, symbol="star", color="red", line=dict(width=2, color="darkred")),
    ))
fig_mesh.update_layout(
    xaxis_title="Number of Elements (millions)",
    yaxis_title="|Volume-Avg Tangential Velocity| (m/s)",
    title="Mesh Independence — Tangential Velocity Convergence",
    template="plotly_white", height=450,
)
st.plotly_chart(fig_mesh, use_container_width=True)

st.markdown("### Selected Meshes for Publication")
st.dataframe(FINAL_MESHES, use_container_width=True, hide_index=True)

col1, col2 = st.columns(2)
with col1:
    st.metric("10-Mesh Basket", "2.15M elements", delta="Inner: 1.91M | Outer: 240K")
with col2:
    st.metric("20-Mesh Basket", "7.49M elements", delta="Inner: 7.25M | Outer: 240K")

st.markdown("""
> **Why 3.5× more cells for 20-mesh?** The 20-mesh basket has wire openings of 0.86 mm 
> (wire diameter 0.406 mm) vs the 10-mesh basket's 1.90 mm openings (wire diameter 0.635 mm). 
> The finer mesh requires denser computational grid to resolve the flow through each opening.
> 
> **Mesh quality:** Orthogonal quality = 0.76 (1 = best), Equi-skewness = 0.23 (0 = best).  
> **Mesh type:** Unstructured tetrahedral/prism, non-conformal grid with 5 inflation layers 
> at vessel wall (growth rate 1.2).
""")
