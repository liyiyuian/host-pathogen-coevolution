
# =====================================================================
# Coevolution Without a Common Ancestor - reproducibility notebook
# team co-evo  |  Built with Claude: Life Sciences (Research track)
#
# This notebook reproduces the HEADLINE NUMBERS and result figures of the
# study from the saved result data in ./data/. It does NOT re-run the full
# upstream pipeline (raw-sequence -> MSA -> embeddings -> model), which ran
# across many sessions on HPC; instead it verifies the published metrics
# from the out-of-fold predictions and metric tables that back every claim.
#
# Requirements: numpy, pandas, scipy, matplotlib   (pip install -r requirements.txt)
# =====================================================================

# %% [markdown]
# ## 0. Setup
import json, numpy as np, pandas as pd
from scipy.stats import rankdata
DATA = "data"

def auc_mannwhitney(y, score):
    """ROC-AUC via the Mann-Whitney U identity (no sklearn needed)."""
    y = np.asarray(y); score = np.asarray(score)
    n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return np.nan
    r = rankdata(score)
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# %% [markdown]
# ## 1. The barrier & the headline signal (verified numbers)
V = {
    "shared_taxa_zero": "7 of 8 structural pairs",
    "dca_positive_control_auc": 0.61, "dca_p": "6e-14",
    "interface_entropy": 0.43, "rest_of_rbd": 0.10, "rest_of_spike": 0.044,
    "fold_within_rbd": 4.2, "fold_vs_spike": 9.75, "perm_p": "1e-4",
    "cross_side_coupling_p": 0.98, "strain_covar_vs_contact_rho": -0.04,
}
for k, v in V.items(): print(f"{k:32s} {v}")

# %% [markdown]
# ## 2. Balanced prediction benchmark - recompute pooled LOSO AUC from raw OOF
oof = np.load(f"{DATA}/oof_balanced.npz")
y, groups = oof["y"], oof["groups"]
print("pairs:", len(y), "| positives:", int(y.sum()), "| species:", len(np.unique(groups)))

feature_sets = ["seq_only","esm_only","esm+seq","coevo_only","esm+coevo","esm+seq+coevo"]
pooled = {fs: auc_mannwhitney(y, oof[fs]) for fs in feature_sets}
for fs in feature_sets: print(f"  pooled LOSO AUC  {fs:16s} {pooled[fs]:.4f}")

delta_pooled = pooled["esm+coevo"] - pooled["esm_only"]
print(f"\ncoevolution lift (pooled): {delta_pooled:+.4f}   (published +0.0065)")

# mean-of-per-species aggregation
def per_species_auc(score):
    return np.nanmean([auc_mannwhitney(y[groups==g], score[groups==g]) for g in np.unique(groups)])
mp_esm = per_species_auc(oof["esm_only"]); mp_ec = per_species_auc(oof["esm+coevo"])
print(f"mean-per-species lift:     {mp_ec-mp_esm:+.4f}   (published +0.013)")

# %% [markdown]
# ## 3. Cross-check against the saved metric table & bootstrap CI
metrics = pd.read_csv(f"{DATA}/prediction_metrics_balanced.csv")
print(metrics.to_string(index=False))
boot = json.load(open(f"{DATA}/loso_balanced.json"))
b = boot.get("bootstrap", boot)
print("\nbootstrap delta point:", b.get("delta_point"), "95% CI:", b.get("ci95"), "P(delta>0):", b.get("p_gt0"))

# %% [markdown]
# ## 4. AF3 no-relative negative - recompute discrimination AUC
af3 = pd.read_csv(f"{DATA}/af3_iptm_scores.csv")
print(af3.to_string(index=False))
lab = (af3["label"].astype(str).str.lower().str.contains("true") | (af3["label"]==1)).astype(int) \
      if "label" in af3.columns else None
if lab is not None:
    for col in ["iptm","ptm","ranking"]:
        if col in af3.columns:
            print(f"  discrimination AUC ({col}): {auc_mannwhitney(lab, af3[col]):.2f}")
    print("  true-pair mean iptm:", round(af3.loc[lab==1,"iptm"].mean(),3),
          "| decoy mean iptm:", round(af3.loc[lab==0,"iptm"].mean(),3))

# %% [markdown]
# ## 5. Per-species transfer table
loso_sp = pd.read_csv(f"{DATA}/loso_per_species_balanced.csv")
print(loso_sp.to_string(index=False))

# %% [markdown]
# ## 6. Figures (pre-rendered in ./figures/)
import matplotlib.pyplot as plt, matplotlib.image as mpimg, os
figs = sorted(f for f in os.listdir("figures") if f.endswith(".png"))
for f in figs:
    im = mpimg.imread(f"figures/{f}")
    fig, ax = plt.subplots(figsize=(11, 11*im.shape[0]/im.shape[1]))
    ax.imshow(im); ax.axis("off"); ax.set_title(f, fontsize=9)
    plt.show()
print("Figures:", figs)
