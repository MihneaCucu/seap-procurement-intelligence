# Profilul și stadiul datelor SEAP

> Raport de inventariere și evaluare a pregătirii datelor pentru analiză. Cifrele provin din manifestul surselor și raportul importului local.

## Rezumat executiv

- **Perioadă:** 2024–2025, toate trimestrele T1–T4.
- **Surse:** 2 seturi oficiale data.gov.ro; licența indicată în catalog: Creative Commons Attribution 4.0.
- **Resurse descărcate:** 16 (8 fișiere de achiziții directe, 8 de contracte).
- **Înregistrări importate:** 5,627,434 (4,581,926 achiziții directe; 1,045,508 contracte publicate).
- **Surse brute:** 1,005,713,727 bytes (aprox. 1.006 GB zecimali); ocupă circa 959 MiB pe discul local.
- **Parquet:** 211,738,377 bytes (aprox. 211.7 MB zecimali; circa 202 MiB pe disc), 21.1% din dimensiunea surselor.
- **Stadiu:** extrase și parsate în Parquet; încă nu sunt standardizate semantic într-o schemă comună.

## Ce înseamnă „procesate”

Fișierele au fost citite, rândurile extrase și salvate în Parquet, partiționat după tip, an și trimestru. Pentru CSV-ul atipic al achizițiilor directe din T1 și T2 2024 există parser dedicat care reconstruiește descrierile întinse pe mai multe linii. Pentru Excel au fost citite foile de date. Antetele originale sunt păstrate; celulele goale sunt reprezentate ca valori nule în raportul importului.

Valorile sunt încă text. Nu s-au făcut conversia semantică a datelor și sumelor în tipuri calendaristice/numerice, maparea sinonimelor dintre antete, deduplicarea, validarea completă a CPV-urilor sau verificări de consistență între exporturi. Se pot explora tabelele individuale; comparațiile agregate între ani necesită standardizare și control al calității.

## Volum pe ani

| An | Achiziții directe | Contracte publicate | Total |
|---:|---:|---:|---:|
| 2024 | 2,347,641 | 415,684 | 2,763,325 |
| 2025 | 2,234,285 | 629,824 | 2,864,109 |
| **Total** | **4,581,926** | **1,045,508** | **5,627,434** |

## Volum pe trimestru

| An | Trim. | Achiziții directe | Contracte publicate | Total |
|---:|:---:|---:|---:|---:|
| 2024 | T1 | 574,373 | 21,433 | 595,806 |
| 2024 | T2 | 618,512 | 161,174 | 779,686 |
| 2024 | T3 | 541,347 | 137,660 | 679,007 |
| 2024 | T4 | 613,409 | 95,417 | 708,826 |
| 2025 | T1 | 500,390 | 124,086 | 624,476 |
| 2025 | T2 | 616,106 | 210,099 | 826,205 |
| 2025 | T3 | 514,263 | 143,317 | 657,580 |
| 2025 | T4 | 603,526 | 152,322 | 755,848 |

Numărul de rânduri este numărul de înregistrări parsate din exportul trimestrial. Nu dovedește de la sine că data fiecărui rând cade exclusiv în trimestrul din numele fișierului; pentru interpretarea temporală trebuie verificate câmpurile de dată și regulile de publicare ale sursei.

## Inventarul fișierelor și importurilor

| An | Trim. | Tip | Format | Fișier sursă | Rânduri | Coloane | Celule nule | % nule | Brut MB | Parquet MB |
|---:|:---:|:---:|:---:|---|---:|---:|---:|---:|---:|---:|
| 2024 | T1 | contracts | CSV | `datagov-raport-contracte-publicate-t-i-2024.csv` | 21,433 | 27 | 2,555 | 0.44% | 9.62 | 0.32 |
| 2024 | T1 | direct | CSV | `datagov-raport-achizitii-directe-t-i-2024.csv` | 574,373 | 13 | 0 | 0.00% | 139.95 | 22.80 |
| 2024 | T2 | contracts | CSV | `datagov-raport-contracte-publicate-t-ii-2024.csv` | 161,174 | 27 | 17,221 | 0.40% | 72.52 | 2.31 |
| 2024 | T2 | direct | CSV | `datagov-raport-achizitii-directe-t-ii-2024.csv` | 618,512 | 13 | 0 | 0.00% | 150.01 | 24.81 |
| 2024 | T3 | contracts | XLS | `datagov-raport-contracte-tiii.xls` | 137,660 | 27 | 13,318 | 0.36% | 57.86 | 2.07 |
| 2024 | T3 | direct | XLS | `datagov-raport-achizitii-directe-tiii.xls` | 541,347 | 14 | 528,304 | 6.97% | 148.24 | 23.99 |
| 2024 | T4 | contracts | XLSX | `datagov-raport-contracte-t-iv_2024.xlsx` | 95,417 | 21 | 3,448 | 0.17% | 9.62 | 1.56 |
| 2024 | T4 | direct | XLSX | `datagov-raport-achizitii-directe-t-iv_2024.xlsx` | 613,409 | 14 | 597,270 | 6.95% | 72.24 | 26.47 |
| 2025 | T1 | contracts | XLSX | `datagov_raport_contracte_t1_2025.xlsx` | 124,086 | 21 | 2,729 | 0.10% | 12.48 | 1.73 |
| 2025 | T1 | direct | XLSX | `datagov_raport-achizitii_directe_t1_2025.xlsx` | 500,390 | 14 | 488,554 | 6.97% | 63.12 | 22.02 |
| 2025 | T2 | contracts | XLSX | `contracte-t2-2025.xlsx` | 210,099 | 21 | 7,648 | 0.17% | 20.86 | 2.58 |
| 2025 | T2 | direct | XLSX | `achizitii-directe-t2-2025.xlsx` | 616,106 | 14 | 599,826 | 6.95% | 77.82 | 27.60 |
| 2025 | T3 | contracts | XLSX | `datagov-contracte-tiii-2025.xlsx` | 143,317 | 21 | 3,405 | 0.11% | 14.36 | 1.95 |
| 2025 | T3 | direct | XLSX | `datagov-achizitii-directe-tiii-2025.xlsx` | 514,263 | 14 | 502,384 | 6.98% | 65.51 | 23.06 |
| 2025 | T4 | contracts | XLSX | `contracte-t_iv_2025.xlsx` | 152,322 | 21 | 2,861 | 0.09% | 15.37 | 2.12 |
| 2025 | T4 | direct | XLSX | `achiziii-directe-t_iv_2025.xlsx` | 603,526 | 14 | 589,010 | 6.97% | 76.13 | 26.33 |

### Distribuția formatelor brute

- CSV: 4 resurse, T1–T2 2024 (achiziții directe și contracte).
- XLS: 2 resurse, T3 2024.
- XLSX: 10 resurse, T4 2024 și toate trimestrele 2025.
- Parquet: 16 fișiere importate, unul pentru fiecare categorie/an/trimestru.

## Ce informații conțin

**Achiziții directe:** identificatori ai achiziției, autoritate contractantă și CUI, denumirea achiziției, cod/denumire CPV, date de publicare și atribuire/finalizare, valoare estimată ori atribuită, ofertant și CUI. În unele versiuni apar tipul contractului, finanțarea comunitară și programul.

**Contracte publicate:** autoritate și CUI, în unele versiuni tipul autorității/activității, anunț și procedură, legislație, tipul și forma contractului, criteriu de atribuire, CPV, numere de anunț/lot/contract, date de publicare și contract, valoare în RON, ofertant și uneori oraș/țară. Câmpurile diferă între versiuni.

## Scheme și coloane

În cele 16 tabele se găsesc **5 variante de schemă**, grupate după lista exactă de antete: trei la achiziții directe și două la contracte. Același număr de coloane nu garantează aceeași semnificație.

### contracts: 27 coloane

Întâlnită în 2024 T1, 2024 T2, 2024 T3.

`Autoritate contractanta`, `CUI`, `Tip autoritate`, `Tip activitate`, `Tip anunt`, `Tip procedura`, `Tip legislatie`, `Tip incheiere contract`, `Tip contract`, `Modalitate de desfasurare`, `Cu licitatie electronica?`, `Tip criteriu de atribuire`, `Cod CPV`, `Denumire CPV`, `Numar anunt initiere`, `Data publicare`, `Numar lot`, `Numar anunt atribuire`, `Data publicare.1`, `Data contract`, `Numar contract`, `Incheiar prin`, `Valoare contract (RON)`, `Ofertant`, `CUI ofertant`, `Oras`, `Tara`

### contracts: 21 coloane

Întâlnită în 2024 T4, 2025 T1, 2025 T2, 2025 T3, 2025 T4.

`Autoritate contractanta`, `CUI autoritate contractanta`, `Tip anunt`, `Tip procedura`, `Numar anunt initiere`, `Data publicare`, `Tip legislatie`, `Tip incheiere contract`, `Tip contract`, `Tip criterii de atribuire`, `Cod CPV`, `Denumire CPV`, `Numar lot`, `Numar anunt atribuire`, `Data publicare.1`, `Data contract`, `Numar contract`, `Incheiat prin`, `Valoare contract (RON)`, `Ofertant castigator`, `CUI ofertant castigator`

### direct: 13 coloane

Întâlnită în 2024 T1, 2024 T2.

`NUMAR_ACHIZITIE_DIRECTA`, `DATA_PUBLICARE_ACHIZITIE`, `STARE_ACHIZITIE`, `DENUMIRE_AC`, `CUI_AC`, `DENUMIRE_ACHIZITIE`, `COD_CPV`, `DENUMIRE_CPV`, `DATA_ATRIBUIRE_ACHIZITIE`, `VALOARE_ESTIMATA_RON`, `VALOARE_ATRIBUITA_RON`, `OFERTANT`, `CUI_OFERTANT`

### direct: 14 coloane

Întâlnită în 2024 T3.

`Autoritate contractanta`, `CUI autoritate`, `Numar achizitie`, `Data publicare`, `Denumire`, `Cod CPV`, `Denumire CPV`, `Tip contract`, `Fonduri comunitare?`, `Denumire program`, `Data atribuire`, `Valoare atribuita (RON)`, `Ofertant castigator`, `CUI ofertant castigator`

### direct: 14 coloane

Întâlnită în 2024 T4, 2025 T1, 2025 T2, 2025 T3, 2025 T4.

`Autoritate contractanta`, `CUI autoritate contractanta`, `Numar achizitie directa`, `Data publicare`, `Denumire achizitie`, `Cod CPV`, `Denumire CPV`, `Tip contract`, `Finantare prin fonduri comunitare?`, `Denumire program`, `Data finalizare`, `Valoare achizitie (RON)`, `Ofertant castigator`, `CUI ofertant castigator`

## Observații de calitate și interpretare

1. **Scheme schimbate în timp.** Contractele au 27 de coloane în T1–T3 2024 și 21 în T4 2024–2025. Achizițiile directe au 13 coloane în T1–T2 2024, 14 în T3 2024, o schemă de 14 în T4 2024 și schema de 14 coloane folosită în 2025.
2. **Valori lipsă.** Raportul conține numărul de celule nule pe tabel. La achizițiile directe T3 2024–2025, aproximativ 6.9–7.0% din toate celulele sunt nule; pentru achizițiile directe T1–T2 2024 raportul indică zero. Diferența trebuie verificată față de codificarea valorilor goale din fiecare sursă înainte de a o interpreta ca diferență reală de completitudine.
3. **Date și numere.** Valorile fiind text, agregările financiare, sortarea calendaristică și comparațiile numerice cer conversii explicite și reguli pentru separatori/valori invalide.
4. **Sume.** Valoarea estimată, valoarea atribuită, valoarea achiziției și valoarea contractului sunt concepte diferite. Nu trebuie însumate împreună fără reguli documentate; nu reprezintă automat prețuri unitare.
5. **Identificatori și duplicate.** CUI, numărul achiziției/anunțului/contractului și lotul pot ajuta la legare, dar cheile candidate și relațiile unu-la-mai-mulți trebuie verificate înaintea deduplicării.
6. **CPV.** Codurile și descrierile sunt prezente, dar normalizarea și validarea nu fac parte din importul actual.
7. **Perioade și versiuni.** Înaintea trendurilor trebuie stabilit dacă exporturile conțin versiuni repetate, înregistrări publicate cu întârziere sau contracte cu mai multe loturi.

## Analize posibile acum și pașii următori

**Explorare imediată:** numărări și distribuții pentru fiecare fișier trimestrial; frecvențe de CPV și autorități; inspecții preliminare ale ofertanților, valorilor, datelor și valorilor lipsă. Rezultatele trebuie să păstreze proveniența fișierului și schema.

**Pentru comparații între ani și trimestre:**

1. dicționar de date cu maparea antetelor variante la câmpuri canonice, păstrând și antetul original;
2. conversie controlată pentru date, sume RON, CUI, identificatori și CPV;
3. profilarea lipsurilor, duplicatelor, formatelor invalide și valorilor extreme pe sursă;
4. reguli de legare între achiziții, anunțuri, contracte, loturi și ofertanți;
5. tabele canonice separate pentru achiziții directe și contracte, cu proveniență an/trimestru/fișier;
6. verificarea totalurilor și refacerea raportului de calitate după standardizare.

Importul este complet la nivel de extragere în Parquet; pregătirea pentru analiză integrată este parțială.

## Localizarea datelor și fișierelor

- Brute: `data/raw/{2024,2025}/`.
- Parquet: `data/processed/{direct,contracts}/year=YYYY/quarter=tN.parquet`.
- Manifest surse: `data/source_manifest.json`.
- Raport import: `data/processed/import_report.json`.
- Sursele brute și Parquet sunt excluse din Git; codul, manifestul și documentația pot fi versionate.

## Proveniență și limite

Inventarul folosește cele 16 resurse din `data/source_manifest.json` și raportul `data/processed/import_report.json`. Dimensiunile surselor sunt cele declarate în catalog la colectare; cele Parquet sunt măsurate la import. Numărul de rânduri este numărul de rânduri parsate, nu o confirmare a unicității și nici o măsură a valorii monetare totale.
