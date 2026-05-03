import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from data import D_BASKET, T_VESSEL, UTIP, sidebar_about

st.set_page_config(page_title="CFD Knowledge Base", page_icon="📖", layout="wide")
sidebar_about()

st.header("📖 CFD Knowledge Base")
st.markdown("Select a topic below to get expert insights from this study.")

TOPICS = [
    ("🔧 Which turbulence model?", "turbulence"),
    ("🔲 Mesh guidelines", "mesh"),
    ("⚡ Power number", "power"),
    ("📸 PIV validation", "piv"),
    ("🔄 Mixing time", "mixing"),
    ("⚙️ Full CFD setup recipe", "setup"),
]

ANSWERS = {
    "turbulence": """
### Turbulence Model Recommendation for USP-1 Basket

Based on systematic testing of 4 RANS models (Sirasitthichoke et al., CES 2023, Fig. 5), 
**Realizable k-ε with Standard Wall Functions** is recommended for USP-1 basket simulations:

1. **Convergence:** Only model achieving residuals < 10⁻⁴ for all variables
2. **PIV Agreement:** Velocity profiles in substantial agreement with experimental PIV data 
   (Sirasitthichoke et al., 2021a)
3. **y⁺ < 5** maintained at all solid surfaces (basket, shaft, vessel wall)
4. **k-ω (Low Re)** was also tested but comparison with PIV "was not favorable" (CES 2023, Section 2)

| Model | Wall Treatment | Converged? | Matches PIV? |
|-------|---------------|:----------:|:------------:|
| k-ω (Low Re) | Integrated | ✗ | ✗ |
| Standard k-ε | Enhanced Wall Treatment | ✗ | ✗ |
| Realizable k-ε | Enhanced Wall Treatment | ✗ | ✗ |
| **Realizable k-ε** | **Standard Wall Functions** | **✓** | **✓** |

*Note:* The convergence criterion was set to residuals < 10⁻⁴ for all velocity magnitudes and 
mass continuity, with ~12,000 iterations needed (CES 2023, Section 3.3).
""",
    "mesh": """
### Mesh Independence Guidelines

*Source: Sirasitthichoke et al. (2023), CES 280, Section 3.2, Fig. 4*

**Grid independence** was verified by monitoring volume-averaged turbulent energy dissipation 
rate (ε) and turbulent kinetic energy (k) as a function of number of cells (Fig. 4 in CES 2023). 
For the 10-mesh basket, grid independence was achieved above ~1.4 million cells.

| Basket Mesh | Final Elements | Inner Domain | Outer Domain |
|:-----------:|:--------------:|:------------:|:------------:|
| 10-mesh | **2,145,850** | 1,906,308 | 239,542 |
| 20-mesh | **7,494,294** | 7,254,752 | 239,542 |

**Mesh quality metrics:**
- Average orthogonal quality: 0.76 (1 = best)
- Average equi-skewness: 0.23 (0 = best)
- 5 inflation layers at vessel wall (growth rate 1.2)
- Unstructured tetrahedral/prism, non-conformal grid

**Why 20-mesh needs 3.5× more cells:** The finer basket wires (0.86 mm openings vs 1.90 mm 
for 10-mesh) require denser mesh to resolve the flow through each opening.
""",
    "power": """
### Power Number in USP-1 Basket

At Re ≈ 1075 (100 RPM, water at 20 °C):

| Basket | Torque (N·m) | Power (W) | Po |
|:------:|:-----------:|:---------:|:---:|
| 10-mesh | 4 × 10⁻⁶ | 4.2 × 10⁻⁵ | **3.53 × 10⁻⁴** |
| 20-mesh | 1.3 × 10⁻⁵ | 1.35 × 10⁻⁴ | **3.85 × 10⁻⁴** |

The extremely low Po (vs typical impellers Po = 1–6) reflects that the basket is a
cylindrical screen, not an impeller. The 20-mesh basket has **~9% higher Po** due to
finer openings creating more flow resistance.
""",
    "piv": """
### PIV Validation Summary

*Primary PIV data: Sirasitthichoke et al. (2021a), Int. J. Pharm: X, 3, 100078*  
*Mesh size study: Sirasitthichoke et al. (2021b), Int. J. Pharm., 607, 120976*  
*CFD validation: Sirasitthichoke et al. (2023), CES 280, Figs. 6–12*

- **Method:** 2D Particle Image Velocimetry (Nd-YAG laser, 532 nm, CCD camera)
- **Seed particles:** Silver-coated hollow borosilicate glass spheres (2–20 µm)
- **Key planes:** 7 horizontal isosurfaces at Y = 10, 16, 23, 28, 34, 58, 68 mm
- **Three velocity components validated:** Axial (Ua), Radial (Ur), Tangential (Ut)
- **Dimensionless form:** Ua/Utip, Ur/Utip, Ut/Utip vs r/R
- **Utip = 0.133 m/s** (at basket bottom edge radius)
- **Limitation:** PIV could NOT measure inside the basket (optical access blocked)
- **CFD advantage:** Provides velocity everywhere including inside the basket (Figs. 14–15)
- **Flow rate validation:** QB-in and QB-out predicted within 5–13% of PIV (Table 1, CES 2023)
""",
    "mixing": """
### Mixing Time in USP-1

*Source: Pace, Sirasitthichoke, Armenante (2023), Chem. Eng. Res. Des. 194, 705–721*

The flow pattern in USP Apparatus 1 is dominated by:
1. **Strong tangential velocity** around the basket (unbaffled system → swirling flow)
2. **Two axial-radial recirculation loops** — an upper loop and a lower loop
3. **Axial flow through the basket base** — fluid enters from below, exits radially through mesh
4. **Jet near basket top** — from the three-pronged clip, influences overall circulation

| Parameter | Effect on Mixing/Blend Time |
|-----------|----------------------------|
| Basket mesh size | Larger openings (10-mesh) → stronger recirculation → faster mixing |
| Fill volume | 500 mL mixes faster than 900 mL |
| RPM | Higher → shorter blend time (approximately inversely proportional) |
| Clip presence | Generates jet → enhances overall circulation |

**Key insight from CES 2023:** The coning effect observed in USP Apparatus 2 (paddle) may 
NOT occur in USP Apparatus 1 because the axial/radial velocities are stronger in the central 
core region below the basket (Section 5.3).
""",
    "setup": """
### Complete CFD Setup Recipe

*Source: Sirasitthichoke et al. (2023), CES 280, Section 3.3*

| Setting | Value |
|---------|-------|
| Software | ANSYS Fluent 2019 R2 / 2021 R2 |
| Solver | Pressure-based, steady-state, double precision |
| Turbulence | Realizable k-ε |
| Wall Treatment | Standard Wall Functions (y⁺ < 5) |
| Pressure | PRESTO! |
| Momentum | Second-order upwind |
| P-V Coupling | SIMPLE |
| Rotation | Multiple Reference Frame (MRF) — "frozen impeller" |
| Gradient | Least-squares cell-based |
| Convergence | Residuals < 10⁻⁴, ~12,000 iterations |
| Monitoring | Volume-averaged tangential velocity in all domains |

**Boundary Conditions:**
- Basket + shaft + clip → rotating wall (inner MRF zone)
- Vessel wall + hemispherical bottom → stationary no-slip
- Free surface → symmetry (flat surface — confirmed experimentally, no vortex at 100 rpm)
- Fluid: water at 20 °C (ρ = 998 kg/m³, μ = 0.001 Pa·s)
- Reference pressure at liquid surface (Y = 126.8 mm for 900 mL)

**MRF Domain:**
- Inner cylinder: radius = 25 mm, height = 54 mm (Y = 18 to 72 mm)
- Outer domain: everything else up to vessel wall and free surface

**Critical geometry detail:** Include the three-pronged clip connecting basket to shaft — 
it generates a jet that affects the overall flow pattern (Section 5, CES 2023).
""",
}

# Topic buttons
row1 = st.columns(3)
row2 = st.columns(3)
all_cols = row1 + row2

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "turbulence"

for i, (label, key) in enumerate(TOPICS):
    if all_cols[i].button(label, key=f"topic_{key}", use_container_width=True):
        st.session_state.selected_topic = key

st.markdown("---")
st.markdown(ANSWERS[st.session_state.selected_topic])

st.markdown("---")
st.markdown("### Quick Reference Cards")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    **🔧 CFD Setup Recipe**
    - Solver: Pressure-based, steady
    - Turb: Realizable k-ε
    - Wall: Standard Wall Functions
    - P-V: SIMPLE + PRESTO!
    - Rotation: MRF
    - Residuals: < 10⁻⁴
    - y⁺ < 5
    """)
with c2:
    st.markdown("""
    **📐 Mesh Guidelines**
    - 10-mesh → 2.15M elements
    - 20-mesh → 7.49M elements
    - Tet + prism layers
    - Orthogonal quality: 0.76
    - Skewness: 0.23
    - 5 inflation layers
    """)
with c3:
    st.markdown(f"""
    **📊 Key Numbers**
    - Re ≈ 1075 at 100 RPM
    - Po ≈ 3.5–3.9 × 10⁻⁴
    - Utip = {UTIP:.4f} m/s
    - D/T = {D_BASKET / T_VESSEL:.3f}
    - 6 publications
    """)
