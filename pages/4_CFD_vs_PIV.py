import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
from data import IMG, sidebar_about

st.set_page_config(page_title="CFD vs PIV", page_icon="📊", layout="wide")
sidebar_about()

st.header("📊 CFD vs. PIV Validation")
st.markdown("""
CFD velocity predictions (Realizable k-ε, Std Wall Functions) were validated against 
2D-PIV measurements at 7 horizontal planes inside the vessel (Y = 10, 16, 23, 28, 34, 58, 68 mm).

*PIV data: Sirasitthichoke et al. (2021a), Int. J. Pharm: X, 3, 100078*  
*CFD data: Sirasitthichoke et al. (2023), Chem. Eng. Sci., 280, 118946 — Figs. 9–12*  
*Mesh size influence: Sirasitthichoke et al. (2021b), Int. J. Pharm., 607, 120976*
""")

# Hero images
st.markdown("### Velocity Fields — 10-mesh vs 20-mesh Basket")
st.caption("CFD simulation results from the author's original research (ANSYS Fluent, Realizable k-ε).")
col_hero1, col_hero2 = st.columns(2)
with col_hero1:
    st.image(str(IMG / "cfd-10mesh-velocity.png"), caption="10-mesh basket — 2.15M cells", use_container_width=True)
with col_hero2:
    st.image(str(IMG / "cfd-20mesh-velocity.png"), caption="20-mesh basket — 7.49M cells", use_container_width=True)

st.markdown("---")

st.markdown("### Validation Summary")
st.markdown("""
| Region | Heights | Agreement | Notes |
|--------|:-------:|:---------:|-------|
| Below basket | Y = 10, 16, 23 mm | ✅ Good | Tangential velocity dominant; axial upward at center |
| Basket region | Y = 34, 58 mm | ✅ Satisfactory | Less agreement at Y=34 due to jet direction |
| Above basket | Y = 68 mm | ✅ Good | CFD closely matches PIV for all 3 components |

**Key observations from the validation (CES 2023, Section 4.1):**
- Tangential velocity was the **dominant flow component** around the basket (typical unbaffled system)
- CFD predicted perfectly symmetrical flow; PIV showed small deviations from symmetry
- The **radial jet** near the basket top was predicted by CFD but its angle differed slightly from PIV
- PIV could **NOT** measure inside the basket — CFD fills this gap (Figs. 14–15)
""")

st.markdown("---")

st.markdown("### Flow Rate Validation (CES 2023, Table 1)")
st.markdown("CFD-predicted flow rates through the basket vs PIV measurements at 100 RPM, 900 mL:")

flow_validation = pd.DataFrame({
    "Basket": ["10-mesh", "10-mesh", "20-mesh", "20-mesh"],
    "Direction": ["Q_in", "Q_out", "Q_in", "Q_out"],
    "CFD (mL/s)": [8.02, 7.30, 5.69, 6.68],
    "PIV (mL/s)": [7.10, 6.95, 6.50, 6.10],
    "Difference (%)": [12.2, 4.9, 13.3, 9.1],
})
st.dataframe(flow_validation, use_container_width=True, hide_index=True)

st.success("""
**Conclusion:** The Realizable k-ε model with Standard Wall Functions captured the main 
hydrodynamic features of the USP Apparatus 1. Flow rate predictions were within **5–13%** 
of PIV measurements, which is acceptable given the complexity of the basket geometry 
(CES 2023, Section 5.2).
""")
