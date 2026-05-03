# USP Dissolution Apparatus Hydrodynamics Explorer

**Interactive research tool for USP Apparatus 1 (rotating basket) hydrodynamics — validated CFD simulations, PIV experiments, and BCS-guided method development. Built from 5 peer-reviewed publications and a doctoral dissertation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.ces.2023.118946-blue)](https://doi.org/10.1016/j.ces.2023.118946)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Chadakarn23/usp1-hydrodynamics-research)

---

## What Does This Tool Do?

Turns static journal data — velocity fields, turbulence model comparisons, mesh studies, power numbers, mixing times — into interactive visualizations, and connects the hydrodynamic data to **BCS-guided pharmaceutical method development**. No CFD software required.

---

## 11 Pages

### Core Hydrodynamics (from publications)

| Page | What You Can Explore |
|------|----------------------|
| **For Scientists & Engineers** | Practical pharma applications — method development, OOS investigation, regulatory justification |
| **Model Selection** | Compare 4 RANS turbulence models — convergence behavior and PIV agreement |
| **Mesh Independence** | Why a 20-mesh basket needs 3.5× more cells than a 10-mesh |
| **CFD vs PIV** | Validation summary at 7 horizontal planes inside the vessel |
| **Flow Rate** | Volumetric flow through the basket — PIV measurements and CFD predictions |
| **Power Number** | Power consumption (Po) across basket mesh sizes |
| **Mixing Time** | Blend time across fill volumes and mesh sizes; sampling representativeness |
| **CFD Knowledge Base** | Turbulence model, mesh, solver, and boundary condition recipe |
| **Publications & About** | Full list of 6 publications + dissertation with DOIs |

### New — BCS Integration & Method Development Tools

| Page | What You Can Do |
|------|-----------------|
| **🧬 BCS Method Development** | Select your compound's BCS class → personalized apparatus recommendations, hydrodynamic sensitivity heatmap, OOS investigation checklist, FDA/EMA/ICH M9 regulatory context |
| **🔢 Condition Calculator** | Input your RPM, temperature, and fill volume → calculate Re, Utip, estimated flow rate, blend time, and power; compare against validated baseline |

---

## Who Is This For?

| Role | Use Case |
|------|----------|
| **Formulation Scientist** | Understand how basket mesh size affects flow around your tablet; get BCS class–specific setup recommendations |
| **Analytical R&D** | Justify dissolution method parameters (mesh, RPM, volume) with validated hydrodynamic data |
| **CMC / Regulatory** | Answer FDA/EMA questions about dissolution method selection backed by 5 peer-reviewed publications and ICH M9 |
| **CFD Engineer** | Validated settings (turbulence model, mesh density, solver, BCs) as a starting point for USP-1 simulations |
| **Student / Researcher** | Benchmark your USP-1 simulations against published PIV and CFD data |
| **Process Engineer** | Trace dissolution variability to hydrodynamic root causes |

---

## Key Finding

Of 4 RANS turbulence models tested, only **Realizable k-ε with Standard Wall Functions** (y⁺ < 5) achieved both convergence (residuals < 10⁻⁴) and agreement with PIV experiments.

> 100 RPM · 900 mL water at 20°C · Re ≈ 1075 · 10-mesh (2.15M cells) and 20-mesh (7.49M cells)

---

## Quick Start

```bash
git clone https://github.com/Chadakarn23/usp1-hydrodynamics-research.git
cd usp1-hydrodynamics-research
pip install -r requirements.txt
streamlit run app.py
```

Opens at **http://localhost:8501**.

**Requirements:** Python 3.10+ · Streamlit · Plotly · NumPy · Pandas (see `requirements.txt`)

---

## Data Sources

All hydrodynamic data comes from peer-reviewed publications. BCS and regulatory guidance follows FDA, EMA, and ICH M9 official documents.

### Hydrodynamic Publications

| Year | Publication | Journal | Data Used In |
|------|-------------|---------|--------------|
| 2023 | CFD of USP-1 hydrodynamics (10- & 20-mesh) | *Chem. Eng. Sci.* 280, 118946 | Model Selection, Mesh Independence, CFD vs PIV, Power Number |
| 2023 | Blend time in USP-1 (with J. Pace) | *Chem. Eng. Res. Des.* 194, 705–721 | Mixing Time |
| 2022 | Power number in stirred vessels with single baffles | *Chem. Eng. Sci.* 257, 117725 | Power Number, CFD Knowledge Base |
| 2021 | PIV velocity distribution in USP-1 | *Int. J. Pharm: X* 3, 100078 | CFD vs PIV |
| 2021 | Basket mesh size influence on hydrodynamics | *Int. J. Pharm.* 607, 120976 | Flow Rate, BCS Method Development |
| 2021 | PhD Dissertation | NJIT | All pages |

### BCS & Regulatory Guidance References

| Document | Used For |
|----------|----------|
| Amidon et al. (1995) *Pharm. Res.* 12, 413–420 | BCS framework |
| FDA (2000) Guidance for Industry: Waiver of In Vivo BA/BE Studies for IR Solid Oral Dosage Forms Based on BCS | Class I biowaiver criteria |
| EMA/CHMP/QWP/BWP/749073/2018 Guideline on the Investigation of Bioequivalence | Class I and III biowaiver criteria (EMA) |
| ICH M9 (2021) Biopharmaceutics Classification System-Based Biowaivers | Harmonized BCS biowaiver guideline (FDA, EMA, PMDA) |
| WHO TRS 992 Annex 6 (2015) | Class III biowaiver (WHO) |
| Kasim et al. (2004) *Mol. Pharm.* 1(1):85–96 | BCS drug classification examples |

---

## BCS Class Summary

| BCS Class | Solubility | Permeability | Hydro Sensitivity | Biowaiver |
|-----------|:----------:|:------------:|:-----------------:|:---------:|
| **I** | High | High | Low | FDA + EMA ✅ |
| **II** | Low | High | **High** | None ❌ |
| **III** | High | Low | Low–Medium | EMA/WHO only ⚠️ |
| **IV** | Low | Low | **High** | None ❌ |

> **For BCS Class II and IV compounds:** the 10-mesh basket delivers ~70% more flow than the 40-mesh basket (7.03 vs 4.09 mL/s at 100 RPM, 900 mL, PIV data), directly affecting dissolution rate. Mesh selection is a **critical method parameter** that must be qualified.

---

## Condition Calculator — How Scaling Works

The calculator extrapolates from the validated 100 RPM, 20°C baseline using standard dimensional analysis:

| Quantity | Scaling Law | Reference |
|----------|-------------|-----------|
| Flow rate | Q ~ N | Geometric similarity, turbulent regime |
| Blend time | θ ~ 1/N | Nienow (1997) *Chem. Eng. J.* 67, 153 |
| Power | P ~ N³ | Po = P/(ρN³D⁵) = constant |
| Water density | Kell (1975) polynomial in °C | *J. Chem. Eng. Data* 20(1):97–105 |
| Water viscosity | Andrade equation | Reid et al., *Properties of Gases and Liquids*, 5th ed. |

Verified: density 998.21 kg/m³ @ 20°C, 993.33 @ 37°C (literature ±0.04%); viscosity 1.002 mPa·s @ 20°C, 0.690 @ 37°C.

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

See the **Publications & About** page in the app for the complete citation list.

---

## License

MIT — free to use, modify, and redistribute. See [LICENSE](LICENSE).

---

## Author

**Chadakarn Sirasitthichoke, Ph.D.**
- PhD, Chemical Engineering — New Jersey Institute of Technology (2021)
- [LinkedIn](https://www.linkedin.com/in/chadakarn-gift-sirasitthichoke-417979a6/)

> **Personal project disclaimer:** This tool was developed entirely on personal time using the author's own PhD dissertation research (2021) and personal computing resources. All data originates from publicly available peer-reviewed publications.

> *The scientific content — turbulence model selection, mesh independence criteria, CFD–PIV validation, flow rates, power numbers, mixing times, and BCS hydrodynamic guidance — originates entirely from the author's published work. Generative AI was used as a coding accelerator to translate validated research into interactive tooling.*
