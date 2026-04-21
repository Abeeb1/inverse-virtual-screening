import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── TRUE POSITIVES from paper (drug -> list of true positive PDB IDs) ──
TRUE_POSITIVES = {
    # PDE
    "sildenafil":    ["3tge", "3shy"],
    "tadalafil":     ["3tvx"],
    "avanafil":      ["3tge", "3shy"],
    "roflumilast":   ["2qyk", "2qyn"],
    "piclamilast":   ["2qyk", "2qyn"],
    "drotaverine":   ["2qyk", "2qyn"],
    # HDAC
    "mocetinostat":  ["1t67", "1w22", "3sff"],
    # Serine
    "apixaban":      ["3gy2", "3rm2"],
    "rivaroxaban":   ["2bvr", "2g8t"],
    "ximelagatran":  ["2g5n", "3kl6"],
}

def load_rankings(base_dir, method):
    """Load all ranking files for a given method (vina/mdock)."""
    all_data = {}
    families = ["HDAC", "PDE", "Serine"]
    for family in families:
        results_dir = os.path.join(base_dir, f"selectivity_dataset_{method}", family, "results")
        if not os.path.exists(results_dir):
            continue
        for fname in sorted(os.listdir(results_dir)):
            if fname.startswith("ranking_") and (fname.endswith(".csv") or fname.endswith(".txt")):
                drug = fname.replace("ranking_", "").replace(".csv", "").replace(".txt", "")
                fpath = os.path.join(results_dir, fname)
                df = pd.read_csv(fpath)
                df.columns = [c.strip() for c in df.columns]
                df["PDB_ID"] = df["PDB_ID"].str.lower().str.strip()
                score_col = [c for c in df.columns if c != "PDB_ID"][0]
                df = df.rename(columns={score_col: "score"})
                df["drug"] = drug
                df["family"] = family
                all_data[drug] = df
    return all_data

base = "/home/aaa6p3/inverse-virtual-screening"
vina_data = load_rankings(base, "vina")

# ── BUILD HEATMAP PER FAMILY ──
families = {
    "PDE":   ["avanafil", "drotaverine", "piclamilast", "roflumilast", "sildenafil", "tadalafil"],
    "HDAC":  ["mocetinostat"],
    "Serine":["apixaban", "rivaroxaban", "ximelagatran"],
}

fig, axes = plt.subplots(1, 3, figsize=(18, 7),
                          gridspec_kw={"width_ratios": [6, 1, 3]})
fig.patch.set_facecolor("#0f1117")

cmap = plt.cm.RdYlGn  # red = weak, green = strong binding

for ax, (family, drugs) in zip(axes, families.items()):
    drugs_present = [d for d in drugs if d in vina_data]
    if not drugs_present:
        ax.axis("off")
        continue

    # Collect all proteins for this family
    all_proteins = []
    for d in drugs_present:
        all_proteins += list(vina_data[d]["PDB_ID"])
    proteins = sorted(set(all_proteins))

    # Build matrix
    matrix = pd.DataFrame(index=proteins, columns=drugs_present, dtype=float)
    for drug in drugs_present:
        df = vina_data[drug].set_index("PDB_ID")
        for prot in proteins:
            if prot in df.index:
                matrix.loc[prot, drug] = df.loc[prot, "score"]

    # Plot heatmap
    im = ax.imshow(matrix.values.astype(float), cmap=cmap, aspect="auto",
                   vmin=-12, vmax=-6)

    ax.set_xticks(range(len(drugs_present)))
    ax.set_xticklabels([d.capitalize() for d in drugs_present],
                        rotation=35, ha="right", fontsize=9, color="white")
    ax.set_yticks(range(len(proteins)))
    ax.set_yticklabels([p.upper() for p in proteins], fontsize=8, color="white")
    ax.set_facecolor("#0f1117")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#444")

    # Highlight true positives with a white border
    for j, drug in enumerate(drugs_present):
        tps = TRUE_POSITIVES.get(drug, [])
        for i, prot in enumerate(proteins):
            if prot in tps:
                ax.add_patch(mpatches.Rectangle(
                    (j - 0.5, i - 0.5), 1, 1,
                    linewidth=2.5, edgecolor="white", facecolor="none"
                ))

    ax.set_title(f"{family} Proteins", color="white", fontsize=11,
                 fontweight="bold", pad=10)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("Vina Score (kcal/mol)", color="white", fontsize=8)
    cbar.ax.yaxis.set_tick_params(color="white")
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="white", fontsize=7)

# Legend
tp_patch = mpatches.Patch(facecolor="none", edgecolor="white",
                            linewidth=2, label="True Positive Target")
fig.legend(handles=[tp_patch], loc="lower center", ncol=1,
           facecolor="#1a1a2e", edgecolor="#444", labelcolor="white",
           fontsize=10, bbox_to_anchor=(0.5, -0.02))

fig.suptitle("AutoDock Vina — Selectivity Dataset\nDocking Scores Across Protein Targets",
             color="white", fontsize=14, fontweight="bold", y=1.01)

plt.tight_layout()
out = os.path.join(base, "selectivity_heatmap_vina.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {out}")
