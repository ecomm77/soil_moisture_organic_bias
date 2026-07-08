# Zenodo activation checklist

Use this checklist immediately before GRSL submission.

## Current public mirror

- GitHub repository: https://github.com/ecomm77/soil_moisture_organic_bias
- GitHub release: https://github.com/ecomm77/soil_moisture_organic_bias/releases/tag/v20260708
- Release asset: `paper2_GRSL_code_package_20260708.zip`
- Release asset SHA256: `ff0210786277ff77707bbcbe092e277e7fc1735bab1fa243ed38d0eda47a34d8`

## Publish the Zenodo record

1. Log in to Zenodo with the author account.
2. Create or reopen the draft record for `GRSL sensor-family validation code package`.
3. Upload `paper2_GRSL_code_package_20260708.zip`.
4. Use `.zenodo.json` as the metadata source.
5. Confirm that the related identifier points to the GitHub mirror above.
6. Publish the record and copy the final DOI.
7. Verify that `https://doi.org/10.5281/zenodo.21263063` or the final DOI resolves with HTTP 200.

## After DOI activation

Update these local files with the final DOI:

- `README.md`
- `CITATION.cff`
- `.zenodo.json`
- `manuscript_snapshot/paper2_GRSL_letter.tex`
- root manuscript `paper2_GRSL_letter.tex`
- root cover letter `GRSL_cover_letter_20260708.md`

Then rerun:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error paper2_GRSL_letter.tex
cp paper2_GRSL_letter.tex paper2_GRSL_code_package_20260708/manuscript_snapshot/paper2_GRSL_letter.tex
cp paper2_GRSL_letter.pdf paper2_GRSL_code_package_20260708/manuscript_snapshot/paper2_GRSL_letter.pdf
cd paper2_GRSL_code_package_20260708
python3 scripts/check_package_integrity.py
find . -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS.txt
shasum -a 256 -c SHA256SUMS.txt
cd ..
rm -f paper2_GRSL_code_package_20260708.zip
zip -qr paper2_GRSL_code_package_20260708.zip paper2_GRSL_code_package_20260708
unzip -t paper2_GRSL_code_package_20260708.zip
```
