# Public Procurement Intelligence — SEAP România

Nume sugerat pentru depozit: `seap-procurement-intelligence`.

## Date colectate și importate

Prima ingestie folosește exporturile oficiale ADR/SEAP publicate pe [data.gov.ro](https://data.gov.ro/):

- [Achiziții publice 2024](https://data.gov.ro/dataset/achizitii-publice-2024)
- [Achiziții publice 2025](https://data.gov.ro/dataset/achizitii-publice-2025)

Am preluat pentru fiecare trimestru două familii de date: **achiziții directe** și **contracte publicate/atribuite**. Licența din catalog este Creative Commons Attribution 4.0. Inventarul cu URL-urile, ID-urile resurselor, dimensiunile declarate și numele fișierelor este în [`data/source_manifest.json`](data/source_manifest.json).

### Import realizat

| Tip înregistrare | 2024 | 2025 | Total |
| --- | ---: | ---: | ---: |
| Achiziții directe | 2.347.641 | 2.234.285 | 4.581.926 |
| Contracte publicate | 415.684 | 629.824 | 1.045.508 |

Fișierele sursă sunt păstrate în `data/raw/{an}/`. Tabelele Parquet se află în `data/processed/{direct,contracts}/year={an}/quarter=t{1..4}.parquet`; fiecare rând conține metadate de proveniență. Raportul importului este generat în `data/processed/import_report.json`.

## Rulare

Necesită Python 3.10+ și `curl`.

```bash
python3 -m pip install -r requirements.txt
python3 scripts/download_data.py
python3 scripts/import_data.py
```

Scriptul de descărcare verifică dimensiunea fiecărui fișier din catalog. Importul citește toate foile Excel. Exporturile CSV din achizițiile directe 2024 au un format atipic; parserul dedicat reconstruiește inclusiv rândurile cu descrieri pe mai multe linii.

## Înainte de analiză sau modele

Schemele diferă între ani și trimestre, deci păstrăm antetele sursă. Valorile sunt importate ca text, iar celulele goale devin valori nule; conversia datelor și sumelor, normalizarea, deduplicarea și validarea CPV rămân pași separați. Achizițiile directe și contractele sunt păstrate separat. Câmpurile de valoare nu sunt automat prețuri unitare; încă nu am construit modele sau recomandări.

Exporturile brute și tabelele Parquet sunt excluse din Git prin `.gitignore`, deoarece seturile sunt voluminoase și pot fi regenerate din manifest.
