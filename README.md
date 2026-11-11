# SEAP Procurement Intelligence

A Romania-focused data pipeline for collecting and preparing public procurement exports published through Romania's official open data portal, [data.gov.ro](https://data.gov.ro/).

## Team dataset

The project links the private [seap-data](https://github.com/MihneaCucu/seap-data) repository through the `dataset/` Git submodule. Dataset v1 contains screened analytical outputs for 2007–2025. Its release manifest pins the files, checksums and row counts used by the team.

After accepting the private repository invitation and signing in with `gh auth login`, run:

```bash
git submodule update --init dataset
python3 dataset/download.py
python3 -m pip install -r dataset/requirements.txt
python3 dataset/build_local_database.py
```

Open `dataset/files/procurement.duckdb` in read-only mode. Keep its Parquet files in the same directory. The [dataset README](https://github.com/MihneaCucu/seap-data#readme) explains access, schema and version updates.

## Data collected

- **Coverage:** 2007–2025 across the catalog periods available in this collection. Direct purchases and contracts are quarterly for 2019–2025; older years include contracts and, for selected years, subsequent contracts at annual, semester, or quarterly granularity.
- **Imported records:** **20,412,240** total: 16,224,190 direct purchases, 4,082,601 published contracts, and 105,449 subsequent contracts.
- **Sources:** 11 official catalog packages and 86 downloaded resources (CSV: 45, XLS: 10, XLSX: 31).
- **Local storage:** 7.666 GB of raw sources and 1.590 GB of Parquet output. Large data files are excluded from Git.
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

The original exports have been parsed with source provenance retained. The local relational build normalizes dates and amounts, filters unusable rows and exact duplicates, and applies ONRC, CPV and privacy checks. Dataset v1 publishes the screened internal analytical views through the private dataset repository. Unresolved identities and approximate duplicate candidates remain available for further review.

## Additional Romanian sources

The profile documents official Romanian sources to assess next, including Ministry of Health public-hospital procurement exports, annual procurement plans (PAAP), ANAF institutional procurement disclosures, and CNSC decisions.

## Target data model

The unified local dataset uses related entities for organizations, procurement records, winning suppliers, CPV categories, purchased items, source resources, official historical BNR rates and dated currency conversions. See the [relational model and diagram](docs/data-model.md) and [SQL reference schema](schema/data-model.sql). The team release includes the schemas of the actual exported analytical views.

A reproducible relational example from the reviewed 32-row sample is available in [JSON](docs/data-sample-normalized.json):

```bash
python scripts/build_normalized_sample.py
```
