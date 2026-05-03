import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import plotly.graph_objects as go
from data import FLOW_RATE_DATA, FLOW_RATE_CFD, BCS_CLASSES, sidebar_about

st.set_page_config(page_title="Flow Rate", page_icon="🔄", layout="wide")
sidebar_about()

st.header("🔄 Flow Rate Through the Basket")
st.markdown("""
The flow rate entering (Q_in) and leaving (Q_out) the basket were measured experimentally 
with PIV and predicted with CFD. Larger mesh openings allow **significantly more flow** 
through the basket, directly affecting dissolution rates.

*PIV data: Sirasitthichoke et al. (2021b), Int. J. Pharm., 607, 120976*  
*CFD validation: Sirasitthichoke et al. (2023), CES 280, Table 1, Fig. 21*
""")

st.markdown("### Experimental (PIV) Flow Rates")
vol_choice = st.radio("Fill Volume", ["900 mL", "500 mL", "Both"], horizontal=True)

if vol_choice == "Both":
    show_flow = FLOW_RATE_DATA
elif vol_choice == "900 mL":
    show_flow = FLOW_RATE_DATA[FLOW_RATE_DATA["Volume (mL)"] == 900]
else:
    show_flow = FLOW_RATE_DATA[FLOW_RATE_DATA["Volume (mL)"] == 500]

st.dataframe(show_flow, use_container_width=True, hide_index=True)
st.download_button("⬇ Download PIV Flow Rate Data (CSV)", show_flow.to_csv(index=False),
                   file_name="piv_flow_rate_data.csv", mime="text/csv")

fig_flow = go.Figure()
for vol in ([900, 500] if vol_choice == "Both" else [int(vol_choice.split()[0])]):
    subset = FLOW_RATE_DATA[FLOW_RATE_DATA["Volume (mL)"] == vol]
    fig_flow.add_trace(go.Bar(
        x=subset["Basket Mesh"], y=subset["PIV Q_in (mL/s)"],
        name=f"Q_in — {vol} mL",
        text=subset["PIV Q_in (mL/s)"].round(2), textposition="outside",
    ))
    fig_flow.add_trace(go.Bar(
        x=subset["Basket Mesh"], y=subset["PIV Q_out (mL/s)"],
        name=f"Q_out — {vol} mL",
        text=subset["PIV Q_out (mL/s)"].round(2), textposition="outside",
    ))
fig_flow.update_layout(
    barmode="group", yaxis_title="Flow Rate (mL/s)",
    title="PIV-Measured Flow Rates Entering and Leaving the Basket",
    template="plotly_white", height=450,
)
st.plotly_chart(fig_flow, use_container_width=True)

st.markdown("---")

st.markdown("### CFD vs PIV Flow Rate Comparison (900 mL, 100 RPM)")
st.markdown("*From CES 2023, Table 1 — CFD predictions within 5–13% of PIV measurements*")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**10-mesh basket**")
    fig_10 = go.Figure()
    fig_10.add_trace(go.Bar(x=["Q_in", "Q_out"], y=[8.02, 7.30], name="CFD", marker_color="#1f77b4"))
    fig_10.add_trace(go.Bar(x=["Q_in", "Q_out"], y=[7.10, 6.95], name="PIV", marker_color="#ff7f0e"))
    fig_10.update_layout(barmode="group", yaxis_title="mL/s", height=350, template="plotly_white", title="10-mesh: CFD vs PIV")
    st.plotly_chart(fig_10, use_container_width=True)
    st.markdown("Q_in difference: **12.2%** | Q_out difference: **4.9%**")

with col2:
    st.markdown("**20-mesh basket**")
    fig_20 = go.Figure()
    fig_20.add_trace(go.Bar(x=["Q_in", "Q_out"], y=[5.69, 6.68], name="CFD", marker_color="#1f77b4"))
    fig_20.add_trace(go.Bar(x=["Q_in", "Q_out"], y=[6.50, 6.10], name="PIV", marker_color="#ff7f0e"))
    fig_20.update_layout(barmode="group", yaxis_title="mL/s", height=350, template="plotly_white", title="20-mesh: CFD vs PIV")
    st.plotly_chart(fig_20, use_container_width=True)
    st.markdown("Q_in difference: **13.3%** | Q_out difference: **9.1%**")

st.info("""
**Key insight:** Larger mesh openings (10-mesh: 1.90 mm) allow ~70% more flow through
the basket than finer mesh (40-mesh: 0.40 mm). This means a tablet inside a 10-mesh basket
is exposed to higher velocities, enhancing solid–liquid mass transfer and faster dissolution.
""")

st.markdown("---")
st.markdown("### 🧬 BCS Class Implications of Flow Rate Differences")
st.markdown("Select your compound's BCS class to see what the flow rate data means for you:")

bcs_pick = st.radio("BCS Class:", ["I", "II", "III", "IV"],
                    format_func=lambda k: f"Class {k} — {BCS_CLASSES[k]['solubility']} S / {BCS_CLASSES[k]['permeability']} P",
                    horizontal=True, key="flow_bcs")
cls = BCS_CLASSES[bcs_pick]
if bcs_pick in ["II", "IV"]:
    st.error(f"""
    **BCS Class {bcs_pick} — High hydrodynamic sensitivity.**
    For {cls['examples'][0]}-type compounds, the 70% flow difference between 10-mesh and 40-mesh
    directly translates into different dissolution rates. This is a **critical method parameter**
    that must be specified and controlled in your dissolution method.
    Recommended mesh: **{cls['mesh_rec']}**
    → Use the [BCS Method Development page](/BCS_Method_Development) for full guidance.
    """)
else:
    st.success(f"""
    **BCS Class {bcs_pick} — Low hydrodynamic sensitivity.**
    For {cls['examples'][0]}-type compounds, dissolution is rapid regardless of mesh choice.
    The 70% flow difference between 10-mesh and 40-mesh has minimal impact on bioavailability.
    Standard 10-mesh at 100 RPM is appropriate.
    → See [BCS Method Development page](/BCS_Method_Development) for complete recommendations.
    """)
