# SEAP Procurement Intelligence

An open data pipeline for collecting and preparing Romania's public procurement exports from SEAP for analysis.

## Current data coverage

The current import covers all four quarters of 2024 and 2025. It contains **5,627,434 records** across 16 quarterly exports:

| Record type | 2024 | 2025 | Total |
| --- | ---: | ---: | ---: |
| Direct purchases | 2,347,641 | 2,234,285 | 4,581,926 |
| Published contracts | 415,684 | 629,824 | 1,045,508 |
| **Total** | **2,763,325** | **2,864,109** | **5,627,434** |

## Sources

The source files are published on Romania's official open data portal, [data.gov.ro](https://data.gov.ro/), by the Authority for the Digitalization of Romania. They contain public information from SEAP and are listed under the [2024](https://data.gov.ro/dataset/achizitii-publice-2024) and [2025](https://data.gov.ro/dataset/achizitii-publice-2025) public procurement datasets. The catalog lists the Creative Commons Attribution 4.0 license. Resource URLs, IDs, declared sizes, and local filenames are recorded in [`data/source_manifest.json`](data/source_manifest.json).

## Download and import

Requires Python 3.10+ and `curl`.

```bash
python3 -m pip install -r requirements.txt
python3 scripts/download_data.py
python3 scripts/import_data.py
```

The downloader checks each file against its catalog size. The importer reads the Excel source sheets and handles the unusual multiline CSV records in the 2024 direct purchase exports.

## Output layout

- Raw source files: `data/raw/{year}/`
- Parquet tables: `data/processed/{direct,contracts}/year={year}/quarter=t{1..4}.parquet`
- Import counts, schemas, and null-cell counts: `data/processed/import_report.json`
- Detailed dataset inventory and readiness report (Romanian): [`docs/PROFIL_DATE_SEAP.md`](docs/PROFIL_DATE_SEAP.md)

Raw exports and generated Parquet tables are excluded from Git because of their size. They can be regenerated from the source manifest and download script.

## Processing status

The source files have been parsed into Parquet and partitioned by record type, year, and quarter. Original source column names are retained. Schemas differ between source years and quarters; values are currently stored as text, and blank cells are represented as nulls.

The pipeline has not yet standardized fields across exports, converted dates and monetary amounts to semantic types, deduplicated records, or fully validated CPV codes. Direct purchases and published contracts remain separate. Amount fields are not automatically unit prices, and no predictive models or recommendations have been built yet.
