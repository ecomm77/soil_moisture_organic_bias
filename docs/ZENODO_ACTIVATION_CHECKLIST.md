# Zenodo publication record

Use this note to keep the public archive, GitHub release, and local package in sync after DOI activation.

## Published archive

- Zenodo DOI: https://doi.org/10.5281/zenodo.21263063
- Zenodo record: https://zenodo.org/records/21263063
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.21263062
- Zenodo API status checked on 2026-07-08: `state=done`, `submitted=true`, license `cc-by-4.0`.
- GitHub repository: https://github.com/ecomm77/soil_moisture_organic_bias
- GitHub release: https://github.com/ecomm77/soil_moisture_organic_bias/releases/tag/v20260708
- Release asset: `paper2_GRSL_code_package_20260708.zip`

## Re-freeze after DOI insertion

If any manuscript or package text changes after publication, rerun:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error paper2_GRSL_letter.tex
cp paper2_GRSL_letter.tex paper2_GRSL_code_package_20260708/manuscript_snapshot/paper2_GRSL_letter.tex
cp paper2_GRSL_letter.pdf paper2_GRSL_code_package_20260708/manuscript_snapshot/paper2_GRSL_letter.pdf
cp paper2_GRSL_letter_supplement.tex paper2_GRSL_code_package_20260708/manuscript_snapshot/paper2_GRSL_letter_supplement.tex
cp paper2_GRSL_letter_supplement.pdf paper2_GRSL_code_package_20260708/manuscript_snapshot/paper2_GRSL_letter_supplement.pdf
cd paper2_GRSL_code_package_20260708
python3 scripts/check_package_integrity.py
find . -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS.txt
shasum -a 256 -c SHA256SUMS.txt
cd ..
rm -f paper2_GRSL_code_package_20260708.zip
zip -qr paper2_GRSL_code_package_20260708.zip paper2_GRSL_code_package_20260708
unzip -t paper2_GRSL_code_package_20260708.zip
```

Then upload the regenerated zip to the GitHub release with `--clobber`. If the already-published Zenodo file should also contain these DOI-inserted metadata files, replace the file via Zenodo's published-file edit window or create a new version from record 21263063.
