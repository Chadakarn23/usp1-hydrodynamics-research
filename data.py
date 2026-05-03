"""
Shared data and constants for the Dissolution Apparatus Hydrodynamics Explorer.
All data from peer-reviewed publications — see Publications & About page for sources.
"""
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

APP_DIR = Path(__file__).parent
IMG = APP_DIR / "images"

# ─── Constants ────────────────────────────────────────────────────────────────
D_BASKET = 0.02546       # basket diameter (m) — per CES 2023 Fig. 1
T_VESSEL = 0.1006        # vessel inner diameter (m) — per CES 2023 Fig. 1
R_VESSEL = T_VESSEL / 2
R_BASKET = D_BASKET / 2
RPM = 100
N = RPM / 60.0
UTIP = np.pi * D_BASKET * N  # tip speed (m/s) ≈ 0.133
RHO = 998.0              # water at 20°C (kg/m³)
MU = 0.001               # water at 20°C (Pa·s)
RE = RHO * N * D_BASKET**2 / MU  # ≈ 1075

# ─── Model Selection ─────────────────────────────────────────────────────────
MODEL_SELECTION = pd.DataFrame({
    "Case": ["(a)", "(b)", "(c)", "(d)"],
    "Turbulence Model": [
        "k-ω (Low Re)", "Standard k-ε", "Realizable k-ε", "Realizable k-ε",
    ],
    "Wall Treatment": [
        "Low-Re (integrated)", "Enhanced Wall Treatment",
        "Enhanced Wall Treatment", "Standard Wall Functions",
    ],
    "Residual Convergence": [
        "Did not converge", "Did not converge", "Did not converge", "< 10⁻⁴ ✓",
    ],
    "PIV Agreement": ["✗", "✗", "✗", "✓"],
    "Notes": [
        "Comparison with PIV was not favorable (CES 2023, Sec. 2)",
        "Over-predicted near-wall turbulence",
        "Over-predicted near-wall turbulence",
        "Best qualitative match — selected for all subsequent simulations",
    ],
})

# ─── Mesh Independence ───────────────────────────────────────────────────────
MESH_INDEP = pd.DataFrame({
    "Mesh Name": [
        "meshindep18", "meshindep19", "meshindep14", "meshindep22",
        "meshindep1", "meshindep8", "meshindep5", "meshindep17",
    ],
    "Elements": [
        1_035_318, 1_256_276, 1_329_833, 1_885_357,
        2_946_990, 3_179_812, 4_083_642, 6_124_010,
    ],
    "Basket Mesh": [None, None, 10, None, None, None, None, None],
    "Tangential Velocity (m/s)": [
        -0.018, -0.019, -0.0185, -0.01845,
        -0.0183, -0.0183, -0.018, -0.018,
    ],
    "Converged": [False, True, True, True, True, True, True, True],
})

FINAL_MESHES = pd.DataFrame({
    "Basket Mesh Size": [10, 20],
    "Elements": [2_145_850, 7_494_294],
    "Inner Domain": [1_906_308, 7_254_752],
    "Outer Domain": [239_542, 239_542],
    "Tangential Velocity (m/s)": [-0.019, -0.018],
})

# ─── Power Consumption ───────────────────────────────────────────────────────
POWER_DATA = pd.DataFrame({
    "Basket Mesh": [10, 20],
    "Elements": [2_145_850, 7_494_294],
    "Density (kg/m³)": [998.2, 998.2],
    "Viscosity (Pa·s)": [0.001003, 0.001003],
    "RPM": [100, 100],
    "D (m)": [0.02546, 0.02546],
    "Re": [1075.18, 1075.18],
    "Torque (N·m)": [4e-6, 1.3e-5],
    "Power (W)": [4.2e-5, 1.35e-4],
    "Po": [0.000353, 0.000385],
    "y+ Note": ["< 5", "< 5"],
})

# ─── Flow Rate ────────────────────────────────────────────────────────────────
FLOW_RATE_DATA = pd.DataFrame({
    "Basket Mesh": ["10-mesh", "20-mesh", "40-mesh", "10-mesh", "20-mesh", "40-mesh"],
    "Volume (mL)": [500, 500, 500, 900, 900, 900],
    "Wire Opening (mm²)": [3.61, 0.7396, 0.1444, 3.61, 0.7396, 0.1444],
    "PIV Q_in (mL/s)": [6.96, 6.15, 4.12, 7.10, 6.50, 4.19],
    "PIV Q_out (mL/s)": [7.37, 6.69, 4.62, 6.95, 6.10, 3.98],
    "PIV Avg Q (mL/s)": [3.52, 2.47, 1.79, 3.50, 2.57, 1.64],
})

FLOW_RATE_CFD = pd.DataFrame({
    "Basket Mesh": ["10-mesh", "10-mesh", "20-mesh", "20-mesh"],
    "Method": ["CFD", "PIV", "CFD", "PIV"],
    "Q_in (mL/s)": [8.02, 7.10, 5.69, 6.50],
    "Q_out (mL/s)": [7.30, 6.95, 6.68, 6.10],
})

# ─── Publications list ────────────────────────────────────────────────────────
PUBLICATIONS = [
    {
        "year": "2023",
        "title": "Computational Determination of Hydrodynamics in the USP Dissolution Testing Apparatus 1 (Rotating Basket)",
        "authors": "Sirasitthichoke, C., Patel, S., Reuter, K.G., Hermans, A., Bredael, G., Armenante, P.M.",
        "journal": "Chemical Engineering Science, 280, 118946",
        "doi": "10.1016/j.ces.2023.118946",
        "topics": ["CFD", "Realizable k-ε", "10- & 20-mesh baskets", "MRF", "PIV validation"],
        "tabs": "Model Selection, Mesh Independence, CFD vs PIV, Power Number",
    },
    {
        "year": "2023",
        "title": "Experimental Determination and Computational Prediction of Blend Time in the USP Dissolution Testing Apparatus 1",
        "authors": "Pace, J., Sirasitthichoke, C., Armenante, P.M.",
        "journal": "Chemical Engineering Research and Design, 194, 705-721",
        "doi": "10.1016/j.cherd.2023.04.053",
        "topics": ["Mixing time", "Blend time", "Tracer experiments", "CFD prediction"],
        "tabs": "CFD Knowledge Base (Mixing Time)",
    },
    {
        "year": "2022",
        "title": "Power Number and Hydrodynamic Characterization of a Stirred Vessel Equipped with a Retreat-Blade Impeller and Different Types of Pharmaceutical Single Baffles",
        "authors": "Sirasitthichoke, C., Salloum, S., Armenante, P.M.",
        "journal": "Chemical Engineering Science, 257, 117725",
        "doi": "10.1016/j.ces.2022.117725",
        "topics": ["Power number", "RBI impeller", "Single baffles", "Torque measurements"],
        "tabs": "Power Number, CFD Knowledge Base",
    },
    {
        "year": "2021a",
        "title": "Experimental Determination of the Velocity Distribution in USP Apparatus 1 (Basket Apparatus) Using Particle Image Velocimetry (PIV)",
        "authors": "Sirasitthichoke, C., Perivilli, S., Liddell, M.R., Armenante, P.M.",
        "journal": "International Journal of Pharmaceutics: X, 3, 100078",
        "doi": "10.1016/j.ijpx.2021.100078",
        "topics": ["PIV", "Velocity fields", "USP-1 baseline", "10/20/40-mesh"],
        "tabs": "CFD vs PIV Validation",
    },
    {
        "year": "2021b",
        "title": "Influence of Basket Mesh Size on the Hydrodynamics in the USP Rotating Basket Dissolution Testing Apparatus 1",
        "authors": "Sirasitthichoke, C., Patel, S., Reuter, K.G., Hermans, A., Bredael, G., Armenante, P.M.",
        "journal": "International Journal of Pharmaceutics, 607, 120976",
        "doi": "10.1016/j.ijpharm.2021.120976",
        "topics": ["Mesh size effect", "Flow rate through basket", "PIV + CFD"],
        "tabs": "CFD vs PIV, Mesh Independence",
    },
    {
        "year": "2021",
        "title": "PhD Dissertation: Hydrodynamics of USP Dissolution Apparatuses",
        "authors": "Sirasitthichoke, C.",
        "journal": "New Jersey Institute of Technology (NJIT), Department of Chemical Engineering",
        "doi": "",
        "topics": ["Full dissertation", "PIV", "CFD", "Mixing time", "Power consumption"],
        "tabs": "All tabs",
    },
]


# ─── Sidebar About ────────────────────────────────────────────────────────────
def sidebar_about():
    """Render a compact About section in the sidebar."""
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            "**Chadakarn Sirasitthichoke, Ph.D.**"
        )
        st.markdown(
            "[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)]"
            "(https://www.linkedin.com/in/chadakarn-gift-sirasitthichoke-417979a6/) &nbsp; "
            "[![GitHub](https://img.shields.io/badge/GitHub-Repo-black?logo=github)]"
            "(https://github.com/Chadakarn23/usp1-hydrodynamics-research)"
        )
        st.caption("Built with Streamlit + Plotly · AI-accelerated development")
