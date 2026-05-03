# Dissolution Apparatus Hydrodynamics Explorer

**Interactive tool for exploring the hydrodynamics of USP Dissolution Apparatus 1 (basket type) — built on validated CFD simulations and PIV experiments from 5 peer-reviewed publications and a doctoral dissertation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.ces.2023.118946-blue)](https://doi.org/10.1016/j.ces.2023.118946)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Chadakarn23CS/usp1-hydrodynamics)

---

## What does this tool do?

Turns static journal data — velocity fields, turbulence model comparisons, mesh studies, power numbers, mixing times — into interactive visualizations you can explore directly in your browser. No CFD software required.

### 9 Tabs

| Tab | What you can explore |
|-----|---------------------|
| **For Scientists & Engineers** | Practical pharma applications: method development, OOS investigation, regulatory justification |
| **Model Selection** | Compare 4 RANS turbulence models — convergence behavior and PIV agreement |
| **Mesh Independence** | Why a 20-mesh basket needs 3.5x more cells than a 10-mesh |
| **CFD vs PIV** | Validation summary at 7 horizontal planes inside the vessel |
| **Flow Rate** | Volumetric flow through the basket — PIV measurements and CFD predictions |
| **Power Number** | Power consumption (Po) comparison across basket mesh sizes and RPM |
| **Mixing Time** | Blend time data for different fill volumes and mesh sizes |
| **CFD Knowledge Base** | Expert-level guidance on turbulence model, mesh, solver settings |
| **Publications & About** | Full list of 5 publications + dissertation with DOIs — every data point traced to its source |

---

## Who is this for?

| Role | Use case |
|------|----------|
| **Formulation Scientist** | Understand how basket mesh size affects flow around your tablet |
| **Analytical R&D** | Justify dissolution method parameters (mesh, RPM, volume) with validated data |
| **CMC / Regulatory** | Answer FDA questions about dissolution method selection with peer-reviewed evidence |
| **CFD Engineer** | Get validated settings as a starting point for your own USP-1 simulations |
| **Student / Researcher** | Benchmark your simulations against published experimental data |

---

## Quick Start

```bash
git clone https://github.com/Chadakarn23CS/usp1-hydrodynamics.git
cd usp1-hydrodynamics
pip install -r requirements.txt
streamlit run app.py
```

Opens at **http://localhost:8501**.

### Requirements

- Python 3.10+
- Streamlit, Plotly, NumPy, Pandas (see `requirements.txt`)

---

## Data Sources

All data comes from 5 peer-reviewed publications and a doctoral dissertation:

| Year | Publication | Journal |
|------|------------|---------|
| 2023 | CFD of USP-1 hydrodynamics (10- & 20-mesh baskets) | *Chem. Eng. Sci.* 280, 118946 |
| 2023 | Blend time in USP-1 (with J. Pace) | *Chem. Eng. Res. Des.* 194, 705-721 |
| 2022 | Power number in stirred vessels with single baffles | *Chem. Eng. Sci.* 257, 117725 |
| 2021 | PIV velocity distribution in USP-1 | *Int. J. Pharm: X* 3, 100078 |
| 2021 | Basket mesh size influence on hydrodynamics | *Int. J. Pharm.* 607, 120976 |
| 2021 | PhD Dissertation | NJIT |

### Key Operating Conditions

- USP Apparatus 1 (basket type) per USP &lt;711&gt;
- Basket mesh sizes: 10, 20 (CFD) and 10, 20, 40 (PIV)
- 100 RPM, 900 mL water at 20 C
- Re ~ 1075

### Key Finding

Of 4 RANS turbulence models tested, only **Realizable k-e with Standard Wall Functions** achieved both convergence (residuals < 1e-4) and agreement with PIV experiments.

---

## License

MIT — free to use, modify, and redistribute. See [LICENSE](LICENSE).

---

## Citation

Primary CFD reference:
```bibtex
@article{sirasitthichoke2023cfd,
  title={Computational Determination of Hydrodynamics in the USP Dissolution Testing Apparatus 1},
  author={Sirasitthichoke, C. and Patel, S. and Reuter, K.G. and Hermans, A. and Bredael, G. and Armenante, P.M.},
  journal={Chemical Engineering Science},
  volume={280},
  pages={118946},
  year={2023},
  doi={10.1016/j.ces.2023.118946}
}
```

PIV experimental reference:
```bibtex
@article{sirasitthichoke2021piv,
  title={Experimental Determination of the Velocity Distribution in USP Apparatus 1 Using PIV},
  author={Sirasitthichoke, C. and Perivilli, S. and Liddell, M.R. and Armenante, P.M.},
  journal={International Journal of Pharmaceutics: X},
  volume={3},
  pages={100078},
  year={2021},
  doi={10.1016/j.ijpx.2021.100078}
}
```

See the **Publications & About** tab in the app for the complete list.

## Author

**Chadakarn Sirasitthichoke, Ph.D.**
- PhD, Chemical Engineering — New Jersey Institute of Technology
- Current: Senior Data Scientist and Process Modeling Engineer, Bristol Myers Squibb
- [LinkedIn](https://www.linkedin.com/in/chadakarn-gift-sirasitthichoke-417979a6/)
