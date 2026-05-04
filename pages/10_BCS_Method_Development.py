import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from data import (
    BCS_CLASSES, BCS_SENSITIVITY, MESH_FLOW_BCS,
    FLOW_RATE_DATA, D_BASKET, T_VESSEL, N, RHO, MU, RE, UTIP,
    sidebar_about,
)

st.set_page_config(page_title="BCS Method Development", page_icon="💊", layout="wide")
sidebar_about()

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.bcs-hero {
    background: linear-gradient(135deg, #1a3a4f 0%, #1a7ab5 70%, #3ba3d9 100%);
    border-radius: 14px;
    padding: 2rem 2rem 1.5rem;
    color: white;
    margin-bottom: 1.5rem;
}
.bcs-hero h1 { font-size: 2rem; font-weight: 800; margin-bottom: 0.4rem; color: white; }
.bcs-hero p  { font-size: 1rem; opacity: 0.9; margin: 0; line-height: 1.6; }

.bcs-card {
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.5rem;
    border: 2px solid transparent;
    cursor: pointer;
    transition: transform 0.2s;
}
.sensitivity-badge-high   { background:#f8d7da; color:#721c24; border-radius:20px; padding:2px 12px; font-weight:700; font-size:0.85rem; }
.sensitivity-badge-medium { background:#fff3cd; color:#856404; border-radius:20px; padding:2px 12px; font-weight:700; font-size:0.85rem; }
.sensitivity-badge-low    { background:#d4edda; color:#155724; border-radius:20px; padding:2px 12px; font-weight:700; font-size:0.85rem; }

.rec-block {
    background: #f8fafc;
    border-left: 4px solid #1a7ab5;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin: 0.4rem 0;
    font-size: 0.92rem;
    line-height: 1.6;
}
.risk-block {
    background: #fff8f0;
    border-left: 4px solid #e67e22;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin: 0.4rem 0;
    font-size: 0.92rem;
}
.oos-block {
    background: #fdf2f8;
    border-left: 4px solid #9467bd;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin: 0.4rem 0;
    font-size: 0.92rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bcs-hero">
    <h1>💊 BCS-Guided Dissolution Method Development</h1>
    <p>
        Select your compound's BCS class to receive targeted apparatus recommendations,
        hydrodynamic sensitivity analysis, and OOS investigation guidance — all backed
        by validated CFD and PIV data from peer-reviewed publications.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Section 1: BCS Classification Chart ──────────────────────────────────────
st.markdown("## BCS Classification Overview")

col_chart, col_desc = st.columns([1.4, 1])

with col_chart:
    # Build quadrant scatter chart
    rng = np.random.default_rng(42)
    drug_data = []
    for cls_key, cls in BCS_CLASSES.items():
        for i, drug in enumerate(cls["examples"]):
            if cls_key == "I":
                sx, py = rng.uniform(0.6, 0.95), rng.uniform(0.6, 0.95)
            elif cls_key == "II":
                sx, py = rng.uniform(0.05, 0.4), rng.uniform(0.6, 0.95)
            elif cls_key == "III":
                sx, py = rng.uniform(0.6, 0.95), rng.uniform(0.05, 0.4)
            else:
                sx, py = rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.4)
            drug_data.append({
                "Drug": drug, "Solubility": sx, "Permeability": py,
                "Class": f"Class {cls_key}", "Color": cls["color"],
                "Sensitivity": cls["hydro_sensitivity"],
            })

    df_drugs = pd.DataFrame(drug_data)
    fig_quad = go.Figure()

    # Quadrant backgrounds
    quad_configs = [
        (0.5, 1, 0.5, 1, "Class I<br>High S / High P", "#d4edda", 0.3),
        (0, 0.5, 0.5, 1, "Class II<br>Low S / High P",  "#f8d7da", 0.3),
        (0.5, 1, 0,   0.5,"Class III<br>High S / Low P","#fff3cd", 0.3),
        (0,   0.5, 0, 0.5,"Class IV<br>Low S / Low P",  "#e9d8f5", 0.3),
    ]
    for x0, x1, y0, y1, label, fillcolor, opacity in quad_configs:
        fig_quad.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                           fillcolor=fillcolor, opacity=opacity, line_width=0, layer="below")
        fig_quad.add_annotation(x=(x0+x1)/2, y=(y0+y1)/2, text=f"<b>{label}</b>",
                                showarrow=False, font=dict(size=11, color="#333"),
                                opacity=0.6)

    # Drug scatter per class
    for cls_key, cls in BCS_CLASSES.items():
        subset = df_drugs[df_drugs["Class"] == f"Class {cls_key}"]
        fig_quad.add_trace(go.Scatter(
            x=subset["Solubility"], y=subset["Permeability"],
            mode="markers+text", name=f"Class {cls_key}",
            text=subset["Drug"], textposition="top center",
            marker=dict(size=12, color=cls["color"], line=dict(width=1.5, color="white")),
            hovertemplate="<b>%{text}</b><br>Class " + cls_key +
                          f" | Hydro sensitivity: {cls['hydro_sensitivity']}<extra></extra>",
        ))

    fig_quad.add_vline(x=0.5, line_dash="dash", line_color="#888", line_width=1.5)
    fig_quad.add_hline(y=0.5, line_dash="dash", line_color="#888", line_width=1.5)
    fig_quad.update_layout(
        xaxis=dict(title="Solubility →", showticklabels=False, range=[0, 1]),
        yaxis=dict(title="Permeability →", showticklabels=False, range=[0, 1]),
        title="BCS Classification Space — Example Drugs",
        template="plotly_white", height=420,
        legend=dict(orientation="h", yanchor="bottom", y=-0.18),
        margin=dict(t=40, b=60),
    )
    st.plotly_chart(fig_quad, use_container_width=True)

with col_desc:
    st.markdown("### The 4 BCS Classes")
    for cls_key, cls in BCS_CLASSES.items():
        badge_color = {"Low": "#d4edda", "Low–Medium": "#fff3cd", "High": "#f8d7da"}
        badge_text  = {"Low": "#155724",  "Low–Medium": "#856404",  "High": "#721c24"}
        sens = cls["hydro_sensitivity"]
        bc   = badge_color.get(sens, "#f0f0f0")
        bt   = badge_text.get(sens, "#333")
        st.markdown(f"""
        <div style="background:{cls['color_light']}; border-left:4px solid {cls['color']};
                    border-radius:0 8px 8px 0; padding:0.7rem 1rem; margin-bottom:0.6rem;">
            <b style="color:{cls['color']}; font-size:1rem;">Class {cls_key}</b>
            &nbsp;— {cls['solubility']} Solubility / {cls['permeability']} Permeability<br>
            <span style="font-size:0.82rem; color:#555;">{', '.join(cls['examples'][:3])}</span><br>
            <span style="background:{bc}; color:{bt}; border-radius:12px; padding:1px 10px;
                         font-size:0.78rem; font-weight:700;">Hydro sensitivity: {sens}</span>
            {"&nbsp;<span style='background:#c3e6cb; color:#155724; border-radius:12px; padding:1px 10px; font-size:0.78rem; font-weight:700;'>Biowaiver: FDA+EMA</span>" if cls_key == 'I' else ("&nbsp;<span style='background:#fff3cd; color:#856404; border-radius:12px; padding:1px 10px; font-size:0.78rem; font-weight:700;'>Biowaiver: EMA/WHO only</span>" if cls_key == 'III' else "")}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ─── Section 2: Method Development Wizard ─────────────────────────────────────
st.markdown("## Method Development Wizard")
st.markdown("Select your compound's BCS class for personalized apparatus recommendations.")

cls_labels = {
    "I":   "🟢 Class I  —  High S / High P",
    "II":  "🔴 Class II  —  Low S / High P",
    "III": "🟠 Class III  —  High S / Low P",
    "IV":  "🟣 Class IV  —  Low S / Low P",
}
selected = st.radio(
    "BCS Class:",
    options=list(cls_labels.keys()),
    format_func=lambda k: cls_labels[k],
    horizontal=True,
    key="bcs_wizard",
)
cls = BCS_CLASSES[selected]

# Mechanism callout
st.markdown(f"""
<div style="background:{cls['color_light']}; border:2px solid {cls['color']};
            border-radius:10px; padding:1.1rem 1.5rem; margin:1rem 0;">
    <span style="font-size:1.1rem; font-weight:800; color:{cls['color']};">
        BCS Class {selected}: {cls['solubility']} Solubility / {cls['permeability']} Permeability
    </span><br><br>
    <b>Dissolution Mechanism:</b> {cls['mechanism']}<br><br>
    <b>Example compounds:</b> {', '.join(cls['examples'])}
</div>
""", unsafe_allow_html=True)

# Recommendations in 3 columns
r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(f"""
    <div class="rec-block">
        <b>🔲 Recommended Basket</b><br>{cls['mesh_rec']}
    </div>
    <div class="rec-block">
        <b>⚡ Agitation Speed</b><br>{cls['rpm_rec']}
    </div>
    """, unsafe_allow_html=True)
with r2:
    st.markdown(f"""
    <div class="rec-block">
        <b>🧪 Medium</b><br>{cls['medium_rec']}
    </div>
    <div class="rec-block">
        <b>💧 Fill Volume</b><br>{cls['volume_rec']}
    </div>
    """, unsafe_allow_html=True)
with r3:
    biowaiver_tags = {
        "I":   "✅ FDA + EMA eligible (≥85% / 30 min at pH 1.2, 4.5, 6.8)",
        "II":  "❌ Not eligible — in vivo BE study required",
        "III": "⚠️ EMA/WHO eligible only (≥85% / 15 min); FDA requires in vivo BE",
        "IV":  "❌ Not eligible — in vivo BE study required",
    }
    biowaiver_tag = biowaiver_tags[selected]
    st.markdown(f"""
    <div class="rec-block">
        <b>📋 BCS Biowaiver</b><br>{biowaiver_tag}
    </div>
    <div class="rec-block">
        <b>📊 Discriminating Method</b><br>{cls['discriminating_note'][:80]}...
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="risk-block">
    <b>⚠️ Key Risk for Class {selected}:</b> {cls['key_risk']}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── Section 3: Hydrodynamic Sensitivity by Mesh ─────────────────────────────
st.markdown("## How Basket Mesh Choice Affects Your Class")
col_flow, col_table = st.columns([1.4, 1])

with col_flow:
    # Flow rate comparison colored by sensitivity to current BCS class
    is_sensitive = selected in ["II", "IV"]
    bar_colors = ["#1f77b4", "#ff7f0e", "#d62728"] if is_sensitive else ["#2ca02c", "#6fba6f", "#a8d5a2"]
    annotation = "⚠️ HIGH impact for BCS Class II/IV" if is_sensitive else "✅ LOW impact for BCS Class I/III"

    fig_mesh_flow = go.Figure()
    fig_mesh_flow.add_trace(go.Bar(
        x=MESH_FLOW_BCS["Basket Mesh"],
        y=MESH_FLOW_BCS["Q_avg 900mL (mL/s)"],
        marker_color=bar_colors,
        text=[f"{v:.2f} mL/s<br>({r:.0f}%)" for v, r in
              zip(MESH_FLOW_BCS["Q_avg 900mL (mL/s)"], MESH_FLOW_BCS["Relative to 10-mesh (%)"])],
        textposition="outside",
        width=0.5,
    ))
    fig_mesh_flow.update_layout(
        yaxis=dict(title="Average Flow Rate (mL/s)", range=[0, 9]),
        title=f"Basket Flow Rate by Mesh — {annotation}",
        template="plotly_white", height=380,
        showlegend=False,
        annotations=[dict(
            x=0.5, y=1.08, xref="paper", yref="paper",
            text=f"<i>PIV data: Sirasitthichoke et al. (2021b), Int. J. Pharm. 607, 120976</i>",
            showarrow=False, font=dict(size=10, color="#888"),
        )],
    )
    st.plotly_chart(fig_mesh_flow, use_container_width=True)

with col_table:
    st.markdown(f"### Impact for BCS Class {selected}")
    impact_col = "BCS II/IV Impact" if selected in ["II", "IV"] else "BCS I/III Impact"
    display_df = MESH_FLOW_BCS[["Basket Mesh", "Wire Opening (mm)", "Q_avg 900mL (mL/s)",
                                  "Relative to 10-mesh (%)", impact_col]].copy()
    display_df.columns = ["Mesh", "Wire (mm)", "Q avg (mL/s)", "Rel. to 10-mesh", "Impact"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    if selected in ["II", "IV"]:
        st.error(f"""
        **For BCS Class {selected}:** Mesh selection is a critical method parameter.
        10-mesh → 40-mesh reduces flow by **~42%**, directly reducing dissolution rate.
        Always specify and qualify your basket mesh in the method.
        """)
    else:
        st.success(f"""
        **For BCS Class {selected}:** Mesh selection has low impact on bioavailability.
        Standard 10-mesh at 100 RPM is appropriate. Focus on medium pH and temperature.
        """)

    # Download button
    csv = MESH_FLOW_BCS.to_csv(index=False)
    st.download_button("⬇ Download Mesh Flow Data (CSV)", csv,
                       file_name="mesh_flow_rate_data.csv", mime="text/csv")

st.markdown("---")

# ─── Section 4: Sensitivity Heatmap ──────────────────────────────────────────
st.markdown("## Apparatus Parameter Sensitivity by BCS Class")

sens_map = {"Low": 1, "Low–Medium": 2, "Medium": 3, "High": 4}
heatmap_z = BCS_SENSITIVITY[["Class I", "Class II", "Class III", "Class IV"]].map(
    lambda x: sens_map.get(x, 0)).values.tolist()
heatmap_text = BCS_SENSITIVITY[["Class I", "Class II", "Class III", "Class IV"]].values.tolist()

fig_heat = go.Figure(go.Heatmap(
    z=heatmap_z,
    x=["Class I", "Class II", "Class III", "Class IV"],
    y=BCS_SENSITIVITY["Parameter"].tolist(),
    text=heatmap_text,
    texttemplate="%{text}",
    colorscale=[[0, "#d4edda"], [0.25, "#fff3cd"], [0.6, "#ffc107"], [1, "#dc3545"]],
    showscale=True,
    colorbar=dict(
        tickvals=[1, 2, 3, 4],
        ticktext=["Low", "Low–Med", "Medium", "High"],
        title="Sensitivity",
    ),
    zmin=1, zmax=4,
))
fig_heat.update_layout(
    title="How Sensitive is Each BCS Class to Each Apparatus Parameter?",
    template="plotly_white", height=370,
    xaxis=dict(side="top"),
    margin=dict(t=80),
)
st.plotly_chart(fig_heat, use_container_width=True)
st.caption("Medium Composition = pH, surfactant concentration, ionic strength. Basket Centering: USP allows ±2 mm — flow field changes significantly within that tolerance (CES 2023).")

st.markdown("---")

# ─── Section 5: OOS Investigation Guide ───────────────────────────────────────
st.markdown(f"## OOS Investigation Framework — BCS Class {selected}")
st.markdown(f"""
<div class="oos-block">
    <b>🔍 Class {selected} OOS Guidance:</b><br>{cls['oos_guidance']}
</div>
""", unsafe_allow_html=True)

st.markdown("### Step-by-Step OOS Checklist")

if selected in ["II", "IV"]:
    st.markdown(f"""
    BCS Class {selected} is **highly sensitive** to hydrodynamics. Work through these checks in order:
    """)
    checks = [
        ("🔲 Basket Mesh", "Is the correct mesh specified in your method? Is the basket clean, undamaged, and unclogged? A fouled 10-mesh behaves like a finer mesh — reducing flow by up to 42%.", "high"),
        ("📍 Basket Position", "Is the basket centered? USP allows ±2 mm — but CFD data (CES 2023) shows the velocity gradient changes significantly within that range near r/R = 0.25.", "high"),
        ("⚡ RPM Calibration", "Was RPM verified with a calibrated tachometer? ±5 RPM at 100 RPM = 5% change in Re, which affects dissolution rate for Class II/IV.", "high"),
        ("🧪 Medium Composition", "Was the medium freshly prepared? Correct pH? Surfactant (SDS, polysorbate) concentration verified? For Class II/IV, even small surfactant changes greatly affect apparent solubility.", "high"),
        ("🌡️ Temperature", "Was medium temperature 37.0 ± 0.5°C? Viscosity changes ≈ 2% per °C, affecting Re and flow.", "medium"),
        ("💧 Fill Volume", "Was volume correct? 900 mL vs 500 mL gives different mixing times (see Mixing Time page). Concentration gradients persist longer in larger volumes.", "medium"),
        ("🔬 Sample Handling", "Filter change between samples? Adequate discard volume? Spectroscopic interference from excipients?", "low"),
    ]
else:
    checks = [
        ("🧪 Medium pH & Composition", "BCS Class I/III is primarily pH-sensitive. Verify buffer capacity, ionic strength, and pH at 37°C.", "high"),
        ("🌡️ Temperature", "Verify 37.0 ± 0.5°C. Solubility of Class I/III compounds can be temperature-dependent.", "medium"),
        ("🔲 Basket Condition", "Inspect for physical damage or clogs. Less critical for Class I/III but still a good practice.", "low"),
        ("📍 Basket Position", "Low hydrodynamic sensitivity for Class I/III — but verify per SOP.", "low"),
        ("⚡ RPM", "Low sensitivity — but verify as part of standard troubleshooting.", "low"),
        ("🔬 Sample Handling", "Check filter, discard volume, dilution factor, spectroscopic method.", "medium"),
    ]

for step_title, step_detail, priority in checks:
    colors = {"high": ("#f8d7da", "#721c24", "🔴"), "medium": ("#fff3cd", "#856404", "🟡"), "low": ("#d4edda", "#155724", "🟢")}
    bg, fg, dot = colors[priority]
    with st.expander(f"{dot} {step_title} — Priority: {priority.title()}"):
        st.markdown(step_detail)
        if "Basket Mesh" in step_title and selected in ["II", "IV"]:
            st.markdown("→ *See the Flow Rate page to quantify the hydrodynamic impact of mesh changes.*")
        if "Basket Position" in step_title and selected in ["II", "IV"]:
            st.markdown("→ *See the CFD vs PIV page for velocity gradients at r/R = 0.25.*")
        if "Mixing Time" in step_title or "Fill Volume" in step_title:
            st.markdown("→ *See the Mixing Time page for blend time data across conditions.*")

st.markdown("---")

# ─── Section 6: Discriminating Method Guide ───────────────────────────────────
st.markdown("## Discriminating Method Design")

disc_col1, disc_col2 = st.columns(2)
with disc_col1:
    st.markdown(f"""
    ### What Makes a Dissolution Method Discriminating?
    A discriminating method detects **formulation differences** that would affect in vivo performance.
    For BCS Class {selected}:

    {cls['discriminating_note']}

    **General criteria (FDA, ICH M9 2021):**
    - Detects changes in particle size / polymorphic form
    - Detects changes in excipient ratio or binder level
    - Correlates with in vivo data (IVIVC) where available
    - Profiles from two formulations differ by **≥10% at ≥1 time point** (f2 similarity < 50)
    """)
with disc_col2:
    # Radar chart comparing discrimination potential across conditions
    categories = ["BCS I", "BCS II", "BCS III", "BCS IV"]
    fig_disc = go.Figure()
    cond_data = {
        "10-mesh, 100 RPM, biorelevant": [3, 9, 3, 9],
        "20-mesh, 100 RPM, buffer": [2, 6, 2, 6],
        "10-mesh, 50 RPM, buffer": [2, 7, 2, 7],
    }
    colors_disc = ["#1a7ab5", "#ff7f0e", "#2ca02c"]
    for (cond, vals), color in zip(cond_data.items(), colors_disc):
        fig_disc.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=categories + [categories[0]],
            fill="toself", name=cond, line_color=color, opacity=0.6,
        ))
    fig_disc.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        title="Relative Discriminating Power<br>by Condition (qualitative)",
        template="plotly_white", height=360,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=10)),
    )
    st.plotly_chart(fig_disc, use_container_width=True)

st.markdown("---")

# ─── Section 7: Regulatory Context ────────────────────────────────────────────
st.markdown("## Regulatory Context")

reg_data = {
    "Class I":  {
        "fda": "BCS Biowaiver eligible (FDA 2000). Rapid dissolution ≥85% in 30 min must be demonstrated at pH 1.2, 4.5, and 6.8 at 37°C.",
        "ema": "Biowaiver eligible (EMA/CHMP/QWP/BWP/749073/2018). Rapid dissolution ≥85% in 30 min at all three pH values.",
        "method_type": "Simple quality-control method. Non-discriminating acceptable for biowaiver.",
        "key_guidance": "FDA (2000) · EMA/CHMP/QWP/BWP/749073/2018 · ICH M9 (2021) · WHO TRS 992 Annex 6 (2015)",
    },
    "Class II": {
        "fda": "No BCS biowaiver. In vivo BE study required. Dissolution method must be discriminating and reflect in vivo performance.",
        "ema": "No biowaiver. Discriminating dissolution in biorelevant media (FaSSIF/FeSSIF) required for meaningful IVIVC.",
        "method_type": "Discriminating method required. Biorelevant media (FaSSIF/FeSSIF) strongly recommended.",
        "key_guidance": "FDA (2000) · ICH M9 (2021) · ICH Q8(R2) (2009) · EMA/CHMP/QWP/BWP/749073/2018",
    },
    "Class III": {
        "fda": "⚠️ FDA 2000 does NOT include Class III biowaivers. Some FDA review division discretion exists but no formal guidance. In vivo BE study generally required.",
        "ema": "Biowaiver eligible (EMA/CHMP/QWP/BWP/749073/2018) with strict criteria: ≥85% in 15 min at pH 1.2, 4.5, and 6.8; no excipient concern; same qualitative composition.",
        "method_type": "EMA/WHO biowaiver possible. Confirm rapid dissolution (≥85% / 15 min). Non-discriminating method acceptable for biowaiver pathway.",
        "key_guidance": "EMA/CHMP/QWP/BWP/749073/2018 · ICH M9 (2021) · WHO TRS 992 Annex 6 (2015) · Amidon et al. (1995) Pharm. Res. 12, 413",
    },
    "Class IV": {
        "fda": "No BCS biowaiver. Most challenging class. In vivo BE study required.",
        "ema": "No biowaiver. Complex formulation strategy and biorelevant dissolution required.",
        "method_type": "Biorelevant media (FaSSIF/FeSSIF) required for meaningful IVIVC. pH-gradient dissolution helpful.",
        "key_guidance": "FDA (2000) · ICH M9 (2021) · ICH Q8(R2) (2009) · EMA/CHMP/QWP/BWP/749073/2018",
    },
}

reg = reg_data[f"Class {selected}"]
rc1, rc2 = st.columns(2)
with rc1:
    st.info(f"**🇺🇸 FDA Perspective:**  \n{reg['fda']}")
    st.info(f"**🇪🇺 EMA Perspective:**  \n{reg['ema']}")
with rc2:
    st.markdown(f"""
    **Method Type Required:**
    {reg['method_type']}

    **Key Guidance Documents:**
    {reg['key_guidance']}
    """)
    if cls["biowaiver"]:
        st.success("✅ This class may qualify for a BCS-based biowaiver — consult FDA/EMA guidelines for full criteria.")
    else:
        st.warning("⚠️ In vivo bioequivalence study typically required for this BCS class.")

st.markdown("---")

# ─── Footer Citation ───────────────────────────────────────────────────────────
st.caption("""
**Hydrodynamic data sources:** Sirasitthichoke et al. (2021b) Int. J. Pharm. 607, 120976 (PIV flow rates) ·
Sirasitthichoke et al. (2023) Chem. Eng. Sci. 280, 118946 (CFD validation, mesh independence) ·
Pace, Sirasitthichoke, Armenante (2023) Chem. Eng. Res. Des. 194, 705-721 (mixing time).
**BCS & Biowaiver guidance:** Amidon et al. (1995) Pharm. Res. 12, 413-420 (BCS framework) ·
FDA (2000) Guidance for Industry: Waiver of In Vivo BA/BE Studies for IR Solid Oral Dosage Forms Based on BCS ·
EMA/CHMP/QWP/BWP/749073/2018 (Guideline on the Investigation of Bioequivalence) ·
ICH M9 (2021) Biopharmaceutics Classification System-Based Biowaivers ·
WHO TRS 992 Annex 6 (2015) Multisource pharmaceutical products.
""")
