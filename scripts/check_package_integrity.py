#!/usr/bin/env python3
"""Basic local integrity check for the GRSL code package."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "MANIFEST.md",
    "DATA_DICTIONARY.md",
    "REPRODUCIBILITY_NOTES.md",
    "requirements.txt",
    "environment.yml",
    "source_data/family_composition.csv",
    "source_data/family_reference_residuals.csv",
    "source_data/validation_metrics_by_subset.csv",
    "source_data/bias_corrections_by_subset.csv",
    "source_data/reweighting_sensitivity.csv",
    "source_data/temporal_metrics_2021_by_family.csv",
    "source_data/temporal_hp_vs_nonhp_2021.csv",
    "source_data/colocated_pair_summary.csv",
    "source_data/crns_cross_check_summary.csv",
    "source_data/public_data_sources.csv",
    "figures/main/paper_fig3_AB.png",
    "figures/main/downstream_figure.png",
    "figures/supplement/phase2_combined_attribution.png",
    "figures/supplement/family_temporal_real2021.png",
    "manuscript_snapshot/paper2_GRSL_letter.tex",
    "manuscript_snapshot/paper2_GRSL_letter.pdf",
    "manuscript_snapshot/paper2_GRSL_letter_supplement.tex",
    "manuscript_snapshot/paper2_GRSL_letter_supplement.pdf",
    "scripts/rebuild_grsl_summary_figures.py",
    "scripts/legacy_project_scripts/real_matchup_2021.py",
]


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    total_bytes = sum(path.stat().st_size for path in ROOT.rglob("*") if path.is_file())
    if missing:
        print("FAIL: missing required files")
        for path in missing:
            print(f"  - {path}")
        return 1
    print("PASS: required files present")
    print(f"package_root={ROOT}")
    print(f"file_count={sum(1 for path in ROOT.rglob('*') if path.is_file())}")
    print(f"total_size_bytes={total_bytes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
