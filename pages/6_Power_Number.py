import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import plotly.graph_objects as go
from data import POWER_DATA, D_BASKET, T_VESSEL, N, RHO, RE, UTIP, sidebar_about

st.set_page_config(page_title="Power Number", page_icon="⚡", layout="wide")
sidebar_about()

st.header("⚡ Power Consumption Analysis")
st.markdown(f"""
Power number (Po) computed from CFD torque on the rotating basket at Re = {RE:.0f}.

$$P_o = \\frac{{P}}{{\\rho N^3 D^5}}$$

where P = 2πN × Torque, ρ = {RHO} kg/m³, N = {N:.4f} rps, D = {D_BASKET} m.

*Power number methodology from: Sirasitthichoke, Salloum, Armenante (2022), CES 257, 117725*  
*CFD torque data: Sirasitthichoke et al. (2023), CES 280*
""")

col1, col2 = st.columns(2)
with col1:
    st.metric("10-Mesh Basket Po", "3.53 × 10⁻⁴", delta="Torque = 4 × 10⁻⁶ N·m")
with col2:
    st.metric("20-Mesh Basket Po", "3.85 × 10⁻⁴", delta="Torque = 1.3 × 10⁻⁵ N·m")

st.markdown("""
> **Key insight:** The 20-mesh basket has a **~9% higher Po** than the 10-mesh basket, 
> indicating that the finer mesh openings create more resistance to flow, requiring 
> more power to maintain the same rotational speed.
""")

fig_po = go.Figure()
fig_po.add_trace(go.Bar(
    x=["10-mesh", "20-mesh"], y=[0.000353, 0.000385],
    marker_color=["#1f77b4", "#ff7f0e"],
    text=["3.53×10⁻⁴", "3.85×10⁻⁴"], textposition="outside", width=0.5,
))
fig_po.update_layout(
    yaxis_title="Power Number (Po)",
    title="Power Number Comparison — 10-mesh vs 20-mesh Basket",
    template="plotly_white", height=400,
)
st.plotly_chart(fig_po, use_container_width=True)

st.dataframe(POWER_DATA, use_container_width=True, hide_index=True)
