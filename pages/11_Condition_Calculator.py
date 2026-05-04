import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from data import (D_BASKET, T_VESSEL, RHO, MU, RE, N, UTIP, FLOW_RATE_DATA,
                  BLEND_BASELINES_900, BLEND_BASELINES_500, sidebar_about)

st.set_page_config(page_title="Condition Calculator", page_icon="🔢", layout="wide")
sidebar_about()

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.calc-hero {
    background: linear-gradient(135deg, #0e4c75 0%, #1a6b9a 60%, #2a8bbf 100%);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    color: white;
    margin-bottom: 1.5rem;
}
.calc-hero h1 { font-size: 1.8rem; font-weight: 800; color: white; margin-bottom: 0.3rem; }
.calc-hero p  { opacity: 0.9; margin: 0; font-size: 0.95rem; }

.result-card {
    background: #f0f7fc;
    border: 1px solid #bbd9f0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.result-card .val { font-size: 1.6rem; font-weight: 800; color: #0e4c75; }
.result-card .lbl { font-size: 0.82rem; color: #5a6a7a; margin-top: 0.2rem; }

.note-card {
    background: #fff8f0;
    border-left: 4px solid #e67e22;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="calc-hero">
    <h1>🔢 Dissolution Condition Calculator</h1>
    <p>
        Scale hydrodynamic conditions from the validated 100 RPM, 20°C baseline to your
        specific RPM, temperature, and fill volume. Estimates are based on dimensional analysis
        and published PIV/CFD data — always verify with in-house qualification.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Inputs ──────────────────────────────────────────────────────────────────
st.markdown("### Enter Your Dissolution Conditions")

col_in1, col_in2, col_in3 = st.columns(3)
with col_in1:
    rpm_user = st.slider("Agitation Speed (RPM)", min_value=25, max_value=200, value=100, step=5)
    basket_mesh = st.selectbox("Basket Mesh Size", ["10-mesh", "20-mesh", "40-mesh"])

with col_in2:
    temp_c = st.slider("Medium Temperature (°C)", min_value=20, max_value=40, value=37, step=1)
    volume_ml = st.selectbox("Fill Volume (mL)", [500, 900], index=1)

with col_in3:
    medium_type = st.selectbox(
        "Medium Type",
        ["Water (reference)", "0.1 N HCl (pH 1.2)", "Acetate buffer (pH 4.5)",
         "Phosphate buffer (pH 6.8)", "FaSSIF (pH 6.5)", "FeSSIF (pH 5.0)", "SDS 0.5% in buffer"],
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Viscosity and density auto-estimated for aqueous media. For non-aqueous, use expert judgment.")

# ─── Fluid properties as function of temperature ──────────────────────────────
# Water viscosity (Pa·s) — Andrade equation (Reid et al., Properties of Gases and Liquids, 5th ed.)
# Verified: 20°C → 1.002 mPa·s, 37°C → 0.690 mPa·s, 40°C → 0.653 mPa·s
def water_viscosity(T_c):
    return 2.414e-5 * 10 ** (247.8 / (T_c + 273.15 - 140))

# Water density (kg/m³) — Kell (1975) equation, valid 0–100°C, t in CELSIUS
# Kell GS (1975) J. Chem. Eng. Data 20(1):97-105
# Verified: 20°C → 998.21, 37°C → 993.1, 40°C → 992.0 kg/m³
def water_density(T_c):
    t = T_c  # must be in Celsius
    return (999.842594 + 6.793952e-2*t - 9.095290e-3*t**2
            + 1.001685e-4*t**3 - 1.120083e-6*t**4 + 6.536332e-9*t**5)

# FaSSIF/FeSSIF have similar viscosity to water at 37°C
rho_user = water_density(temp_c)
mu_user  = water_viscosity(temp_c)

# Published baseline (100 RPM, 20°C water)
rho_ref = RHO   # 998.0 kg/m³
mu_ref  = MU    # 0.001 Pa·s
N_ref   = N     # 100/60 rps
N_user  = rpm_user / 60.0

# ─── Calculated values ────────────────────────────────────────────────────────
re_user   = rho_user * N_user * D_BASKET**2 / mu_user
utip_user = np.pi * D_BASKET * N_user

# Flow rate scales linearly with N (Q ~ N·D³ for geometrically similar)
# Use 10-mesh 900 mL PIV baseline = 7.03 mL/s avg at 100 RPM
flow_baselines = {"10-mesh": 7.03, "20-mesh": 6.30, "40-mesh": 4.09}
q_ref_mesh = flow_baselines[basket_mesh]
q_user = q_ref_mesh * (N_user / N_ref)

# Mixing time scales inversely with N (θ ~ 1/N)
blend_ref = BLEND_BASELINES_900[basket_mesh] if volume_ml == 900 else BLEND_BASELINES_500[basket_mesh]
blend_user = blend_ref * (N_ref / N_user)

# Power consumption scales as N³
power_baselines = {"10-mesh": 4.2e-5, "20-mesh": 1.35e-4}
power_no_data = basket_mesh not in power_baselines
power_ref_val = power_baselines.get(basket_mesh, power_baselines["10-mesh"])
power_user = power_ref_val * (N_user / N_ref) ** 3

# Regime classification — stirred-tank conventions (Nienow; Holland & Chapman)
# For impeller Re = ρND²/μ in unbaffled tanks: laminar < 10, transitional 10–10⁴, turbulent > 10⁴
if re_user < 10:
    regime = "Laminar"
elif re_user < 1e4:
    regime = "Transitional"
else:
    regime = "Turbulent"

regime_color = {"Laminar": "#28a745", "Transitional": "#fd7e14", "Turbulent": "#dc3545"}

st.markdown("---")
st.markdown("### Calculated Hydrodynamic Conditions")

# Results row 1
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown(f"""<div class="result-card">
    <div class="val">{re_user:.0f}</div>
    <div class="lbl">Reynolds Number (Re)</div>
</div>""", unsafe_allow_html=True)

c2.markdown(f"""<div class="result-card">
    <div class="val">{utip_user*100:.2f} cm/s</div>
    <div class="lbl">Tip Speed (U<sub>tip</sub>)</div>
</div>""", unsafe_allow_html=True)

c3.markdown(f"""<div class="result-card">
    <div class="val">{q_user:.2f} mL/s</div>
    <div class="lbl">Est. Flow Rate ({basket_mesh})</div>
</div>""", unsafe_allow_html=True)

c4.markdown(f"""<div class="result-card">
    <div class="val">{blend_user:.0f} s</div>
    <div class="lbl">Est. Blend Time</div>
</div>""", unsafe_allow_html=True)

c5.markdown(f"""<div class="result-card">
    <div class="val" style="color:{regime_color[regime]};">{regime}</div>
    <div class="lbl">Flow Regime</div>
</div>""", unsafe_allow_html=True)

# Results row 2 — fluid properties
st.markdown("")
cf1, cf2, cf3, cf4 = st.columns(4)
cf1.markdown(f"""<div class="result-card">
    <div class="val">{rho_user:.1f}</div>
    <div class="lbl">Density (kg/m³) @ {temp_c}°C</div>
</div>""", unsafe_allow_html=True)

cf2.markdown(f"""<div class="result-card">
    <div class="val">{mu_user*1000:.3f} mPa·s</div>
    <div class="lbl">Viscosity @ {temp_c}°C</div>
</div>""", unsafe_allow_html=True)

cf3.markdown(f"""<div class="result-card">
    <div class="val">{power_user:.2e} W</div>
    <div class="lbl">Est. Power Consumed</div>
</div>""", unsafe_allow_html=True)

cf4.markdown(f"""<div class="result-card">
    <div class="val">{re_user / RE:.2f}×</div>
    <div class="lbl">Re vs. Published Baseline (100 RPM, 20°C)</div>
</div>""", unsafe_allow_html=True)

if power_no_data:
    st.warning("**Power estimate for 40-mesh:** No published CFD torque data for 40-mesh. Shown value is extrapolated from 10-mesh baseline — treat as a rough order-of-magnitude only.")

st.markdown("---")

# ─── Comparison vs Published Baseline ────────────────────────────────────────
st.markdown("### Your Conditions vs. Published Validated Baseline")

compare_df = pd.DataFrame({
    "Parameter": ["RPM", "Temperature (°C)", "Density (kg/m³)", "Viscosity (Pa·s)",
                  "Re", "Utip (m/s)", f"Flow Rate — {basket_mesh} (mL/s)", "Blend Time (s, est.)"],
    "Published Baseline\n(100 RPM, 20°C, 900 mL)": [
        100, 20, f"{rho_ref:.1f}", f"{mu_ref:.4f}",
        f"{RE:.0f}", f"{UTIP:.4f}", f"{q_ref_mesh:.2f}", f"{blend_ref}",
    ],
    "Your Conditions": [
        rpm_user, temp_c, f"{rho_user:.1f}", f"{mu_user:.4f}",
        f"{re_user:.0f}", f"{utip_user:.4f}", f"{q_user:.2f}", f"{blend_user:.0f}",
    ],
    "Ratio (Yours / Baseline)": [
        f"{rpm_user/100:.2f}×",
        f"—",
        f"{rho_user/rho_ref:.4f}×",
        f"{mu_user/mu_ref:.4f}×",
        f"{re_user/RE:.2f}×",
        f"{utip_user/UTIP:.2f}×",
        f"{q_user/q_ref_mesh:.2f}×",
        f"{blend_user/blend_ref:.2f}×",
    ],
})
st.dataframe(compare_df, use_container_width=True, hide_index=True)

# Deviation warnings
deviations = []
if abs(re_user - RE) / RE > 0.3:
    deviations.append(f"Re = {re_user:.0f} is >{abs(re_user-RE)/RE*100:.0f}% from validated baseline (Re = {RE:.0f}). CFD data may not directly extrapolate.")
if temp_c != 37:
    deviations.append(f"Temperature {temp_c}°C ≠ 37°C (USP standard). Viscosity at {temp_c}°C = {mu_user*1000:.3f} mPa·s vs 0.692 mPa·s at 37°C.")
if rpm_user < 50 or rpm_user > 150:
    deviations.append(f"RPM = {rpm_user} is outside the typical 50–150 RPM range. Non-linear effects may apply at very low or high RPM.")

if deviations:
    st.warning("**Extrapolation Cautions:**\n" + "\n".join(f"- {d}" for d in deviations))

st.markdown("---")

# ─── RPM Sweep Chart ─────────────────────────────────────────────────────────
st.markdown("### Flow Rate & Blend Time vs. RPM — Full Sweep")
st.caption(f"For {basket_mesh}, {volume_ml} mL, {temp_c}°C. Shaded band = range of published mesh conditions.")

rpm_range = np.arange(25, 201, 5)
N_range   = rpm_range / 60.0
q_range   = q_ref_mesh * (N_range / N_ref)
blend_range = blend_ref * (N_ref / N_range)
re_range  = rho_user * N_range * D_BASKET**2 / mu_user

fig_sweep = go.Figure()

fig_sweep.add_trace(go.Scatter(
    x=rpm_range, y=q_range,
    name="Flow Rate (mL/s)", line=dict(color="#1f77b4", width=2.5),
    yaxis="y1",
))
fig_sweep.add_trace(go.Scatter(
    x=rpm_range, y=blend_range,
    name="Blend Time (s)", line=dict(color="#d62728", width=2.5, dash="dot"),
    yaxis="y2",
))

# Mark user's RPM
fig_sweep.add_vline(x=rpm_user, line_dash="dash", line_color="#e67e22",
                     annotation_text=f"Your RPM: {rpm_user}", annotation_position="top right",
                     annotation_font_color="#e67e22")

# Mark published baseline
fig_sweep.add_vline(x=100, line_dash="dot", line_color="#2ca02c",
                     annotation_text="Published baseline: 100 RPM", annotation_position="top left",
                     annotation_font_color="#2ca02c")

fig_sweep.update_layout(
    xaxis=dict(title="RPM", range=[20, 205]),
    yaxis=dict(title="Est. Flow Rate (mL/s)", color="#1f77b4"),
    yaxis2=dict(title="Est. Blend Time (s)", overlaying="y", side="right",
                color="#d62728", range=[0, max(blend_range) * 1.2]),
    template="plotly_white", height=400,
    title=f"Hydrodynamic Scaling — {basket_mesh}, {volume_ml} mL",
    legend=dict(x=0.01, y=0.99),
)
st.plotly_chart(fig_sweep, use_container_width=True)

st.markdown("---")

# ─── Re Regime Chart ─────────────────────────────────────────────────────────
col_re1, col_re2 = st.columns(2)
with col_re1:
    st.markdown("### Reynolds Number Context")
    st.markdown(f"""
    At your conditions ({rpm_user} RPM, {temp_c}°C):

    | | |
    |---|---|
    | **Re** | {re_user:.0f} |
    | **Regime** | {regime} |
    | **vs. Published** | {re_user/RE:.2f}× (baseline Re = {RE:.0f}) |

    **What Re means for dissolution (stirred-tank convention):**
    - Re < 10: Laminar, viscous-dominated
    - Re 10 – 10⁴: Transitional — **all standard USP-1 conditions fall here**
    - Re > 10⁴: Turbulent (would require ~1000 RPM in water — far outside USP range)
    - **Published validated range: Re ≈ 1075 (100 RPM, 20°C water)**

    *Thresholds per Nienow (1997); Holland & Chapman, Liquid Mixing in Stirred Tanks.*

    At **37°C** (USP standard), water viscosity ≈ 0.692 mPa·s vs 1.000 mPa·s at 20°C —
    Re at 37°C is ~1.4× higher for the same RPM.
    """)

with col_re2:
    # Re vs RPM at 37C and 20C comparison
    fig_re = go.Figure()
    for T_c, color, label in [(20, "#1f77b4", "20°C (validated baseline)"),
                               (37, "#d62728", "37°C (USP standard)")]:
        mu_T = water_viscosity(T_c)
        rho_T = water_density(T_c)
        re_T = rho_T * (rpm_range / 60) * D_BASKET**2 / mu_T
        fig_re.add_trace(go.Scatter(
            x=rpm_range, y=re_T,
            name=label, line=dict(color=color, width=2.5),
        ))
    fig_re.add_hline(y=RE, line_dash="dot", line_color="#888",
                     annotation_text=f"Published Re = {RE:.0f}", annotation_position="right")
    fig_re.add_vline(x=rpm_user, line_dash="dash", line_color="#e67e22")
    fig_re.update_layout(
        xaxis_title="RPM", yaxis_title="Reynolds Number (Re)",
        title="Re vs RPM at 20°C and 37°C",
        template="plotly_white", height=340,
    )
    st.plotly_chart(fig_re, use_container_width=True)

st.markdown("---")

# ─── Download ─────────────────────────────────────────────────────────────────
st.markdown("### Export Your Calculation")
export_df = pd.DataFrame({
    "Parameter": ["RPM", "Temperature (°C)", "Mesh", "Volume (mL)", "Medium",
                  "Density (kg/m³)", "Viscosity (Pa·s)", "Re", "Utip (m/s)",
                  "Flow Rate (mL/s)", "Blend Time (s, est.)", "Power (W, est.)", "Flow Regime"],
    "Value": [rpm_user, temp_c, basket_mesh, volume_ml, medium_type,
              f"{rho_user:.2f}", f"{mu_user:.6f}", f"{re_user:.1f}", f"{utip_user:.5f}",
              f"{q_user:.3f}", f"{blend_user:.1f}", f"{power_user:.3e}", regime],
})
csv_out = export_df.to_csv(index=False)
st.download_button("⬇ Download Calculation Results (CSV)", csv_out,
                   file_name=f"condition_calc_{rpm_user}rpm_{temp_c}C_{basket_mesh.replace('-','')}.csv",
                   mime="text/csv")

st.markdown("""
<div style="background:#f8fafc; border:1px solid #dde; border-radius:8px; padding:1rem; font-size:0.85rem; color:#666; margin-top:1rem;">
<b>⚠️ Disclaimer:</b> Flow rate and blend time estimates are extrapolated from validated 100 RPM, 20°C, 900 mL PIV/CFD data
using dimensional scaling (Q ~ N, θ ~ 1/N, P ~ N³). These are approximations valid within the transitional Re regime.
They are not a substitute for apparatus qualification and method validation at your specific conditions.
Published data: Sirasitthichoke et al. (2021b, 2023), Pace et al. (2023).
</div>
""", unsafe_allow_html=True)
