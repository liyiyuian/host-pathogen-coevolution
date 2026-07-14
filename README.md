# Coevolution Without a Common Ancestor
### Reading the host–pathogen arms race from strain variation alone

**Team co-evo — liyiyuian (Ian Lee)** · Built with Claude: Life Sciences (Research Track)

A study of co-evolutionary signals in host–pathogen protein interactions, built entirely in Claude Science. Classical direct-coupling analysis needs a shared species tree; humans and their pathogens share none. We identify the co-evolutionary signal that survives that barrier — readable from the strain sequences genomic surveillance already collects.

## What's here

| File | Description |
|------|-------------|
| [`index.html`](index.html) | Landing page — the project at a glance |
| [`scientific_report.html`](scientific_report.html) | Full scientific report (Background → Hypotheses → Methods → Results → Conclusion) |
| [`scientific_report.pdf`](scientific_report.pdf) | PDF version of the report |
| [`demo_animation.html`](demo_animation.html) | Self-contained animated demo explainer |

## Key findings

- **The barrier.** Across 8 experimentally-solved host–pathogen complexes, 7 share *zero* taxa — the paired alignment DCA requires cannot be built. A co-speciating positive control (Ras/Rho GTPases) recovers contacts at AUC 0.61 (p = 6×10⁻¹⁴), proving the method works; the missing shared history is what breaks it.
- **The signal.** SARS-CoV-2 receptor-binding residues that contact ACE2 vary 4.2× more across strains than the rest of the domain (permutation p = 1×10⁻⁴) — computable with no paired alignment and no shared tree.
- **Generality.** Significant in 3 of 8 systems; fold-change alone misleads, so we gate on an absolute-entropy floor.
- **Model enhancement.** A species-balanced leave-one-species-out benchmark (13 species, 9,172 pairs) shows transfer tracks phylogenetic proximity (AUC 0.49 → 0.80); a lightweight arms-race feature helps 8/13 species.
- **Structure (a negative).** AlphaFold-3 interface confidence does not discriminate true from decoy pairs for a phylogenetically isolated pathogen (pooled AUC 0.50, n = 7; shallow-MSA caveat).

## Two demonstrated applications

1. **Escape-residue early warning** from surveillance sequences.
2. **An honest cross-species benchmark** that exposes phylogenetic leakage.

## View online

With GitHub Pages enabled (Settings → Pages → Deploy from branch `main`, root), the site is served at:
`https://liyiyuian.github.io/built-with-claude-life-sciences-coevo/`

---

*Built entirely in Claude Science. Product/journal-style presentation of a research study; independent work, not affiliated with any company or publisher.*
