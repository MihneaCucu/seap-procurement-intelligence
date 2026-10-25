# SEAP Procurement Intelligence

A Romania-focused data pipeline for collecting and preparing public procurement exports published through Romania's official open data portal, [data.gov.ro](https://data.gov.ro/).

## Data collected

- **Coverage:** 2007–2025 across the catalog periods available in this collection. Direct purchases and contracts are quarterly for 2019–2025; older years include contracts and, for selected years, subsequent contracts at annual, semester, or quarterly granularity.
- **Imported records:** **20,412,265** total: 16,224,211 direct purchases, 4,082,605 published contracts, and 105,449 subsequent contracts.
- **Sources:** 11 official catalog packages and 86 downloaded resources (CSV: 45, XLS: 10, XLSX: 31).
- **Local storage:** 7.666 GB of raw sources and 1.525 GB of Parquet output. Large data files are excluded from Git.
- **Licenses:** vary by source package/year. 2021–2025 list CC BY 4.0; older packages list OGL-ROU-1.0. Check the manifest before reuse.

Coverage is not uniform across years. See the [Romanian data profile](docs/PROFIL_DATE_SEAP.md) for exact per-year counts, all 86 source files, licenses, parsing limitations, and additional Romanian government data sources under consideration.

## Download and import

Requires Python 3.10+, `curl`, and the packages in `requirements.txt`.

```bash
python3 -m pip install -r requirements.txt
python3 scripts/download_data.py
python3 scripts/import_data.py
```

## Local layout

- Raw exports: `data/raw/{year}/` and `data/raw/historical/`
- Parquet tables: `data/processed/{direct,contracts,contracts_subsequent}/year=YYYY/quarter=...parquet`
- Import counts and source schemas: `data/processed/import_report.json`
- Source IDs, URLs, sizes, and licenses: `data/source_manifest.json`

## Processing status

The source exports have been downloaded and parsed into 86 Parquet tables. Original columns and source provenance are retained, while values remain text. The data has **not** been semantically standardized, deduplicated, or fully validated, so cross-year analysis still needs a canonical schema and data-quality review. Legacy free-text fields need additional review because some files have inconsistent encodings, delimiters, and multiline descriptions.

## Additional Romanian sources

The profile documents official Romanian sources to assess next, including Ministry of Health public-hospital procurement exports, annual procurement plans (PAAP), ANAF institutional procurement disclosures, and CNSC decisions.
