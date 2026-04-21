# 🔍 Inverse Virtual Screening for Target Identification

> **Identifying protein targets for bioactive compounds using large-scale molecular docking pipelines**

---

## 🧬 Overview

Most drug discovery starts with a known disease target and searches for a molecule that binds it. **Inverse virtual screening (IVS) flips this**: given a bioactive molecule, which proteins in the human proteome does it bind — and how selectivity?

This project implements a scalable IVS pipeline that docks a query ligand against a curated panel of protein structures, ranks binding affinities, and predicts the most likely biological targets. It was developed and benchmarked on the **sc-PDB dataset (10,000+ protein-ligand complexes)** and validated against known target-ligand pairs.

**Why it matters:** IVS is critical for polypharmacology profiling, side effect prediction, drug repurposing, and mechanism-of-action elucidation — all high-priority problems in modern pharmaceutical R&D.

---

## ✨ Key Features

- 🏗️ **Scalable docking pipeline** — processes thousands of protein structures in parallel using HPC/cloud infrastructure
- 📦 **Curated benchmark dataset** — validated sc-PDB subset with known binding annotations for reproducible evaluation
- ⚡ **Automated target ranking** — scores and ranks candidate proteins by predicted binding affinity and ligand selectivity
- 📊 **Benchmarking framework** — standardized evaluation metrics (enrichment factor, AUC, ROC) for method comparison
- 🔄 **Flexible docking backends** — modular design supports AutoDock, Glide, and RosettaDock

---

## 🏗️ Pipeline Architecture

```
Query Ligand (SDF/MOL2)
        │
        ▼
┌─────────────────────┐
│  Ligand Preparation │  ← RDKit: 3D conformer generation, protonation
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Protein Library    │  ← sc-PDB curated subset (10,000+ structures)
│  Preparation        │  ← Binding site detection, grid generation
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Parallel Docking   │  ← AutoDock Vina / Glide / RosettaDock
│  (HPC/AWS batch)    │  ← MPI-parallelized across protein panel
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Scoring & Ranking  │  ← Binding energy, enrichment factor, selectivity
└─────────────────────┘
        │
        ▼
   Ranked Target List + Visualization
```

---

## 📁 Repository Structure

```
inverse-virtual-screening/
├── data/
│   ├── benchmark/          # sc-PDB curated benchmark set
│   └── sample_ligands/     # Example query molecules
├── src/
│   ├── prepare_ligands.py  # Ligand 3D prep and protonation
│   ├── prepare_proteins.py # Protein cleaning and grid generation
│   ├── run_docking.py      # Parallelized docking execution
│   ├── score_and_rank.py   # Affinity scoring and target ranking
│   └── evaluate.py         # Benchmark evaluation (EF, AUC, ROC)
├── notebooks/
│   └── results_analysis.ipynb  # Interactive results exploration
├── configs/
│   └── docking_config.yaml     # Docking parameters
├── results/
│   └── benchmark_results.csv   # Precomputed benchmark output
├── requirements.txt
└── README.md
```

---

## 🚀 Quickstart

```bash
# Clone the repository
git clone https://github.com/abeeb1/inverse-virtual-screening.git
cd inverse-virtual-screening

# Install dependencies
pip install -r requirements.txt

# Run IVS on a sample ligand against the benchmark protein panel
python src/run_docking.py --ligand data/sample_ligands/aspirin.sdf --config configs/docking_config.yaml

# Rank and visualize results
python src/score_and_rank.py --results results/docking_output.csv
```

---

## 📊 Results & Benchmarking

### Drugs/sc-PDB Dataset (47 FDA-approved drugs · 901 human proteins)

| Method | Mean EF | Median EF | Cases EF > 50% |
|---|---|---|---|
| AutoDock Vina | 72.6% | 72.0% | 89.4% (42/47) |
| MDock | 74.0% | 75.9% | 93.6% (44/47) |
| ΔVinaXGB (ML rescoring) | 73.9% | 73.2% | 95.7% (45/47) |
| **Consensus Scoring** | **75.1%** | **76.9%** | **93.6% (44/47)** |

> EF = 50% corresponds to random selection. All methods significantly outperform random.

### Enrichment Curve — Top-ranked Fractions

| Method | EC @ Top 5% (mean / median) |
|---|---|
| AutoDock Vina | 24.6% / 16.7% |
| MDock | 21.9% / 16.7% |
| ΔVinaXGB rescoring | 27.0% / 25.0% |

### Selectivity Dataset (10 drugs · 8 protein targets · true positives & negatives)

| Method | Correct target predictions |
|---|---|
| AutoDock Vina | 9 / 10 |
| MDock | 9 / 10 |
| ΔVinaXGB | 7 / 10 |

---

## 🔬 Methods

- **Protein preparation:** Structures sourced from sc-PDB; binding sites defined by co-crystallized ligand positions; grids generated with AutoDock Tools / Glide Receptor Preparation
- **Ligand preparation:** RDKit-based 3D conformer generation; OpenBabel protonation at physiological pH
- **Docking:** [AutoDock Vina / Glide SP / RosettaDock — specify which]
- **Scoring:** Binding free energy estimation; selectivity score computed as rank percentile across protein panel
- **Evaluation:** Enrichment factor at 1% and 5%; AUROC; comparison against known target annotations

---

## 📚 Related Publication

> Ma Z\*, **Ajibade A\*** (co-first author), Zou X. *"Docking strategies for predicting protein-ligand interactions and their application to structure-based drug design."* Commun Inf Syst. 2024;24(3):199–230.

---

## 🛠️ Dependencies

```
Python >= 3.8
RDKit
AutoDock Vina
numpy, pandas, scipy
matplotlib, seaborn
mpi4py (for HPC parallelization)
```

---

## 👤 Author

**Abeeb Ajibade** — PhD Candidate, Computational Biophysics, University of Missouri
[LinkedIn](https://linkedin.com/in/abeeb-ajibade) · [GitHub](https://github.com/abeeb1) · ajibadeabeeb95@gmail.com
