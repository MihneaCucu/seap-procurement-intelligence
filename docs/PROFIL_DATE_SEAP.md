# Profilul și stadiul datelor SEAP

> Inventar și evaluare a datelor colectate din portalul oficial data.gov.ro. Rândurile descriu înregistrări parsate, nu achiziții unice și nici valoare financiară totală.

## Rezumat

- **Interval calendaristic:** 2007–2025 (19 ani). Acoperirea tipurilor diferă pe perioade.
- **Origine:** 11 pachete oficiale data.gov.ro cu exporturi publice SEAP.
- **Resurse brute descărcate:** 86 fișiere; **7,665,519,813 bytes** (7.666 GB zecimali, 7.14 GiB).
- **Formate originale:** CSV: 45, XLS: 10, XLSX: 31.
- **Înregistrări parsate:** **20,412,240**: 16,224,190 achiziții directe, 4,082,601 contracte publicate și 105,449 contracte subsecvente.
- **Tabele procesate:** 86 fișiere Parquet, **1,590,130,859 bytes** (1.590 GB zecimali, 1.48 GiB).
- **Licențe:** variază după pachet/an; vezi tabelul de mai jos și manifestul.

## Ce acoperă anii

| Interval | Acoperire disponibilă în import | Granularitate |
|---|---|---|
| 2007–2011 | Contracte publicate | anual |
| 2012–2015 | Contracte publicate | semestre S1/S2 |
| 2016 | Contracte și contracte subsecvente | semestre S1/S2 |
| 2017 | Contracte și contracte subsecvente | trimestre T1–T4 |
| 2018 | Contracte; contracte subsecvente T1 | trimestre unde există în catalog |
| 2019–2025 | Contracte publicate și achiziții directe | trimestre T1–T4 |

**Volum importat pe an:**

| An | Directe | Contracte | Contracte subsecvente | Total |
|---:|---:|---:|---:|---:|
| 2007 | 0 | 62 220 | 0 | 62 220 |
| 2008 | 0 | 114 602 | 0 | 114 602 |
| 2009 | 0 | 122 353 | 0 | 122 353 |
| 2010 | 0 | 124 347 | 0 | 124 347 |
| 2011 | 0 | 105 688 | 0 | 105 688 |
| 2012 | 0 | 108 038 | 0 | 108 038 |
| 2013 | 0 | 66 644 | 0 | 66 644 |
| 2014 | 0 | 73 827 | 0 | 73 827 |
| 2015 | 0 | 77 099 | 0 | 77 099 |
| 2016 | 0 | 75 368 | 45 480 | 120 848 |
| 2017 | 0 | 102 049 | 41 978 | 144 027 |
| 2018 | 0 | 51 777 | 17 991 | 69 768 |
| 2019 | 2 467 401 | 66 781 | 0 | 2 534 182 |
| 2020 | 2 224 044 | 105 734 | 0 | 2 329 778 |
| 2021 | 2 366 402 | 419 260 | 0 | 2 785 662 |
| 2022 | 2 267 327 | 564 577 | 0 | 2 831 904 |
| 2023 | 2 317 090 | 796 729 | 0 | 3 113 819 |
| 2024 | 2 347 641 | 415 684 | 0 | 2 763 325 |
| 2025 | 2 234 285 | 629 824 | 0 | 2 864 109 |
| **Total** | **16 224 190** | **4 082 601** | **105 449** | **20 412 240** |

Importul selectează contractele și achizițiile directe din pachetele naționale, plus seturile de contracte subsecvente disponibile în 2016–2018. Nu reprezintă toate fișierele asociate fiecărui pachet. Anunțurile de inițiere, modificările de contracte, invitațiile SAD, programele anuale de achiziții (PAAP) și alte familii auxiliare sunt inventariate pentru o etapă separată.

## De unde provin

Toate fișierele de bază provin din pachete oficiale data.gov.ro. Manifestul păstrează ID-ul pachetului și al resursei, URL-ul de descărcare, licența pachetului, dimensiunea măsurată și calea locală. Vezi [Achiziții publice 2023](https://data.gov.ro/dataset/achizitii-publice-2023), [Achiziții publice 2024](https://data.gov.ro/dataset/achizitii-publice-2024) și [Achiziții publice 2025](https://data.gov.ro/dataset/achizitii-publice-2025). Pentru pachetele vechi, metadatele și licențele sunt în [manifestul surselor](../data/source_manifest.json).

### Licența declarată de fiecare pachet

| Pachet/an | Licența declarată în catalog |
|---|---|
| 2024 | Creative Commons Attribution 4.0 |
| 2025 | Creative Commons Attribution 4.0 |
| 2023 | Creative Commons Attribution 4.0 |
| 2022 | Creative Commons Attribution 4.0 |
| 2021 | Creative Commons Attribution 4.0 |
| 2020 | OGL-ROU-1.0 |
| 2019 | OGL-ROU-1.0 |
| 2018 | OGL-ROU-1.0 |
| 2017 | OGL-ROU-1.0 |
| 2016 | OGL-ROU-1.0 |
| 2007-2015 | OGL-ROU-1.0 |

Respectă licența fiecărui pachet și citează data.gov.ro/autoritatea publicatoare. Licențele nu sunt uniforme: pachetele 2021–2025 declară CC BY 4.0, iar pachetele mai vechi declară OGL-ROU-1.0.

## Procesare și pregătirea pentru analiză

Fișierele CSV/XLS/XLSX au fost descărcate și convertite în Parquet. Numele coloanelor originale sunt păstrate; fiecare tabel adaugă `source_year`, `source_quarter`, `record_type`, `source_resource_id`, `source_file` și `source_sheet`. Tipurile rămân separate în `direct`, `contracts` și `contracts_subsequent`.

Aceasta este **extragere și parsare**, nu o schemă analitică armonizată. Valorile rămân text; nu sunt convertite semantic datele și sumele, nu sunt mapate variantele de antete la câmpuri canonice și nu s-a făcut deduplicare. Nu s-a validat complet CPV, CUI, moneda sau consistența între exporturi. Pentru trenduri și agregări financiare trebuie standardizate tipurile și regulile pe ani.

Exporturile legacy au fost mai puțin uniforme decât cele recente: separatoare `^`/`|`, câmpuri cu virgule și descrieri împărțite pe mai multe rânduri. La parsare, descrierile multiline au fost aplatizate; delimitatorii în plus din câteva câmpuri text au fost transformați în spații. Un export legacy a conținut byte-uri invalide pentru codepage-ul detectat, care au fost înlocuite la decodare. Aceste texte trebuie revizuite înaintea analizelor definitive.

### Anomalie de sursă: achiziții directe 2022 T2

CSV-ul de achiziții directe T2 2022 conține **415 941** rânduri de achiziții directe, urmate de un al doilea antet de contracte și șase rânduri anexate. Importul direct se oprește la acel antet ca să nu amestece tipurile. Contractele T2 sunt importate separat din resursa lor oficială proprie. Fișierul brut păstrează segmentul anexat pentru inspecție.

## Alte resurse oficiale românești de investigat

Aceste piste locale nu sunt incluse în tabelele de bază și nu au fost descărcate în această rundă:

1. **Ministerul Sănătății – achizițiile unităților sanitare publice.** [Pachetul 2024](https://data.gov.ro/en/dataset/achizitii-derulate-de-unitatile-sanitare-publice-in-anul-2024) oferă fișiere lunare XLS pentru achiziții directe, anunțuri de inițiere, contracte și loturi neatribuite (48 resurse). Există și [pachetul 2025](https://data.gov.ro/en/dataset/achizitii-derulate-de-unitatile-sanitare-publice-in-anul-2025). Valoare posibilă: filtru sectorial și câmpuri suplimentare; fiind subset pe spitale, probabil se suprapune cu exporturile SEAP și trebuie verificat pe ID-uri înainte de unire.
2. **Planuri anuale de achiziții (PAAP).** Catalogul data.gov.ro listează [Achiziții publice 2013–2016 – PAAP](https://data.gov.ro/dataset?groups=finante&q=achizitii+publice); acestea descriu planificarea, nu rezultatele atribuirii. Pot fi legate ulterior pentru analiza planificat-versus-realizat, după inventarierea fișierelor și licențelor.
3. **ANAF – transparența achizițiilor proprii.** [Pagina ANAF pentru achiziții publice](https://www.anaf.mfinante.gov.ro/anaf/internet/ANAF/info_publice/info_interes_public/lista_achizitii_publice) publică centralizatoare și programe anuale. Este o sursă instituțională, nu o bază națională; formatele și structura trebuie inspectate înainte de ingestie.
4. **CNSC / contestații.** Deciziile pot adăuga rezultatul contestațiilor procedurilor, dar în scanarea aceasta nu am identificat un export național structurat potrivit pentru ingestie; portalul și documentele publice necesită o cercetare separată.

Ordinea recomandată: inspectăm schema și licența fiecărui pachet, descărcăm separat, comparăm ID-urile cu exportul SEAP și păstrăm sursa secundară separată până când suprapunerea e măsurată.

## Inventarul tuturor resurselor importate

Dimensiunile brute sunt măsurate local după descărcare; cele Parquet sunt măsurate după import. `Tip export` corespunde coloanei `record_type`.

| An | Perioadă | Tip export | Format | Rânduri | Coloane | Brute MB | Parquet MB | Sursă |
|---:|:---:|---|:---:|---:|---:|---:|---:|---|
| 2024 | T1 | contracts | CSV | 21 433 | 27 | 9.62 | 0.32 | `datagov-raport-contracte-publicate-t-i-2024.csv` |
| 2024 | T1 | direct | CSV | 574 373 | 13 | 139.95 | 22.80 | `datagov-raport-achizitii-directe-t-i-2024.csv` |
| 2024 | T2 | contracts | CSV | 161 174 | 27 | 72.52 | 2.31 | `datagov-raport-contracte-publicate-t-ii-2024.csv` |
| 2024 | T2 | direct | CSV | 618 512 | 13 | 150.01 | 24.81 | `datagov-raport-achizitii-directe-t-ii-2024.csv` |
| 2024 | T3 | contracts | XLS | 137 660 | 27 | 57.86 | 2.07 | `datagov-raport-contracte-tiii.xls` |
| 2024 | T3 | direct | XLS | 541 347 | 14 | 148.24 | 23.99 | `datagov-raport-achizitii-directe-tiii.xls` |
| 2024 | T4 | contracts | XLSX | 95 417 | 21 | 9.62 | 1.56 | `datagov-raport-contracte-t-iv_2024.xlsx` |
| 2024 | T4 | direct | XLSX | 613 409 | 14 | 72.24 | 26.47 | `datagov-raport-achizitii-directe-t-iv_2024.xlsx` |
| 2025 | T1 | contracts | XLSX | 124 086 | 21 | 12.48 | 1.73 | `datagov_raport_contracte_t1_2025.xlsx` |
| 2025 | T1 | direct | XLSX | 500 390 | 14 | 63.12 | 22.02 | `datagov_raport-achizitii_directe_t1_2025.xlsx` |
| 2025 | T2 | contracts | XLSX | 210 099 | 21 | 20.86 | 2.58 | `contracte-t2-2025.xlsx` |
| 2025 | T2 | direct | XLSX | 616 106 | 14 | 77.82 | 27.60 | `achizitii-directe-t2-2025.xlsx` |
| 2025 | T3 | contracts | XLSX | 143 317 | 21 | 14.36 | 1.95 | `datagov-contracte-tiii-2025.xlsx` |
| 2025 | T3 | direct | XLSX | 514 263 | 14 | 65.51 | 23.06 | `datagov-achizitii-directe-tiii-2025.xlsx` |
| 2025 | T4 | contracts | XLSX | 152 322 | 21 | 15.37 | 2.12 | `contracte-t_iv_2025.xlsx` |
| 2025 | T4 | direct | XLSX | 603 526 | 14 | 76.13 | 26.33 | `achiziii-directe-t_iv_2025.xlsx` |
| 2023 | T1 | contracts | XLS | 226 408 | 27 | 94.38 | 2.96 | `acca52ff-50e6-4668-9fa7-c8b1c9201334_raport-contracte-publicate-t1-2023.xls` |
| 2023 | T2 | contracts | XLS | 198 642 | 27 | 78.38 | 2.53 | `a9ca9109-6016-47ab-bfd1-8ee9fa0b0868_datagov-raport-contracte-publicate-tii-2023.xls` |
| 2023 | T3 | contracts | CSV | 211 460 | 27 | 100.44 | 2.64 | `6ccf50f4-2862-4d32-b616-39e05faa0ee6_datagov-raport-contracte-publicate-t-iii-2023.csv` |
| 2023 | T4 | contracts | CSV | 160 219 | 27 | 72.06 | 2.17 | `1a2d1fff-caec-4e9d-aad8-05a6ef8b954e_datagov-raport-contracte-publicate-t-iv-2023.csv` |
| 2023 | T1 | direct | XLS | 584 116 | 16 | 174.95 | 31.75 | `28f536d5-fa32-4e9f-80a1-07454a1e488c_raport-achizitii-directe-t1-2023.xls` |
| 2023 | T2 | direct | XLS | 593 815 | 16 | 178.82 | 32.73 | `3a8ab998-2a0e-4e42-81b4-7f089e04dfb8_datagov-raport-achizitii-directe-tii-2023.xls` |
| 2023 | T3 | direct | CSV | 529 481 | 16 | 148.41 | 24.63 | `b21a319f-514b-4e15-98a4-5a992caf3813_datagov-raport-achizitii-directe-t-iii-2023.csv` |
| 2023 | T4 | direct | CSV | 609 678 | 13 | 147.43 | 23.69 | `5acf3253-4ea9-4d00-a6c3-3d220b9e9145_datagov-raport-achizitii-directe-t-iv-2023.csv` |
| 2022 | T1 | contracts | CSV | 229 495 | 19 | 68.59 | 4.02 | `40d2ac89-80d9-4ced-9692-cc7f4fbc5be4_raport-contracte-t1-2022.csv` |
| 2022 | T2 | contracts | XLS | 64 862 | 36 | 60.37 | 5.93 | `4ea3ccd1-a543-4e29-be7c-774aaa040912_raport-contracte-t2-2022.xls` |
| 2022 | T3 | contracts | XLS | 116 381 | 36 | 93.58 | 8.82 | `9f8f9dc1-16da-4686-a2eb-c47f1c7d25f3_raport-datagov-contracte-t3-2022.xls` |
| 2022 | T4 | contracts | XLS | 153 839 | 35 | 115.18 | 10.82 | `07490d6d-b45b-4e85-aa6b-c4a6126e5267_raport-datagov-contracte-t4-2022.xls` |
| 2022 | T1 | direct | CSV | 543 491 | 13 | 130.89 | 21.12 | `76fc47a5-69aa-425f-b3e4-67ecd2f41f46_raport-achizitii-directe-t1-2022.csv` |
| 2022 | T2 | direct | CSV | 415 941 | 13 | 126.50 | 16.59 | `9f541d85-c102-4dfc-a6f2-4ad012f375ee_raport-achizitii-directe-t2-2022.csv` |
| 2022 | T3 | direct | CSV | 551 425 | 13 | 133.25 | 22.09 | `b4e53488-facd-4bf3-9030-234c8c6fea8c_raport-datagov-achizitii-directe-t3-2022.csv` |
| 2022 | T4 | direct | CSV | 756 470 | 13 | 182.29 | 30.17 | `1bc1453a-5335-40c0-ae1c-303f9ad1eef0_raport-datagov-achizitii-directe-t4-2022.csv` |
| 2021 | T1 | contracts | XLSX | 57 035 | 36 | 48.63 | 4.57 | `c923a70c-d7b7-4bf8-a1ff-eb025b5cdac0_raport-t-1-2021.xls` |
| 2021 | T2 | contracts | XLS | 96 019 | 36 | 75.73 | 7.19 | `dea44c88-5a0a-4ac9-9fed-3575623ef136_raport-t-2-2021.xls` |
| 2021 | T3 | contracts | CSV | 131 603 | 36 | 256.57 | 8.77 | `e5f2680d-6be9-4db2-a9ba-b3a8c3a1e5ed_raport-contracte-t3.csv` |
| 2021 | T4 | contracts | CSV | 134 603 | 36 | 280.57 | 10.06 | `cd750e45-7e3a-424c-b3be-b0387bddc89d_raport-contracte-t4.csv` |
| 2021 | T1 | direct | XLSX | 460 307 | 21 | 95.95 | 51.44 | `5fb48214-0818-4024-b13e-2eebe6b1a73d_achizitii_directe_2021_t1.xlsx` |
| 2021 | T2 | direct | CSV | 583 038 | 21 | 309.67 | 64.06 | `e5b14dd8-2dc0-432d-9e11-820c9549aed5_achizitii-directe-2021-t2.csv` |
| 2021 | T3 | direct | CSV | 555 262 | 21 | 297.65 | 63.79 | `5f439f08-4187-441c-9220-47c7f3109826_raport-da-t3.csv` |
| 2021 | T4 | direct | CSV | 767 795 | 13 | 185.23 | 30.24 | `a94329f1-471a-4ffe-ba4a-c40033853795_raport-achizitii-directe-t4.csv` |
| 2020 | T1 | contracts | XLSX | 21 160 | 36 | 26.42 | 2.80 | `f0767534-258d-4bf7-aad9-ed4f23de3fae_raport-t-1-2020.xls` |
| 2020 | T2 | contracts | XLSX | 24 114 | 36 | 28.49 | 2.92 | `c1428d5c-4fd1-4130-9560-0f1e0acd430d_raport-t-2-2020.xls` |
| 2020 | T3 | contracts | XLSX | 28 131 | 36 | 33.65 | 3.40 | `f08dd716-f8c8-4096-aa98-87dfe883af5d_raport-t-3-2020.xls` |
| 2020 | T4 | contracts | XLSX | 32 329 | 36 | 37.35 | 3.91 | `accfe438-329f-40cd-848f-9f9d6ffe0515_raport-t-4-2020.xls` |
| 2020 | T1 | direct | XLSX | 547 692 | 21 | 160.14 | 85.32 | `3e827637-6aba-4b47-85c9-e09f05c71057_achizitii_directe_2020_t1.xlsx` |
| 2020 | T2 | direct | XLSX | 441 758 | 21 | 135.01 | 74.46 | `5d1f6b75-24c5-4413-8403-b34a10db2312_achizitii_directe_2020_t2.xlsx` |
| 2020 | T3 | direct | XLSX | 556 561 | 21 | 170.14 | 94.24 | `4a800a9f-dfe9-4f6b-9bff-d418148e2514_achizitii_directe_2020_t3.xlsx` |
| 2020 | T4 | direct | XLSX | 678 033 | 21 | 209.40 | 117.81 | `c7b416e5-3d59-4426-a09e-15f5acc33005_achizitii_directe_2020_t4.xlsx` |
| 2019 | T1 | contracts | XLSX | 9 563 | 36 | 17.38 | 1.83 | `04345127-97ea-4524-bae1-e43d19c58c5d_raport-t-1-2019.xls` |
| 2019 | T2 | contracts | XLSX | 17 560 | 36 | 27.77 | 2.95 | `cd2de7fc-44a7-457b-8315-3e0a92720aa3_raport-t-2-2019.xls` |
| 2019 | T3 | contracts | XLSX | 17 560 | 36 | 27.77 | 2.95 | `522c1615-9898-4843-84da-b49fea56a3d1_raport-t-3-2019.xls` |
| 2019 | T4 | contracts | XLSX | 22 098 | 36 | 33.68 | 3.63 | `bb6a46a7-f608-469d-9a25-751e2266931e_raport-t-4-2019.xls` |
| 2019 | T1 | direct | XLSX | 503 338 | 21 | 140.45 | 72.29 | `4deb36c1-e977-487d-88a9-58a0beaab064_achizitiidirecte2019t1.xlsx` |
| 2019 | T2 | direct | XLSX | 639 990 | 21 | 186.45 | 98.75 | `858ba60e-dc7a-44fa-a6d2-f14d1b4a9037_achizitiidirecte2019t2.xlsx` |
| 2019 | T3 | direct | XLSX | 551 554 | 21 | 161.33 | 87.55 | `6591543a-5055-4cf3-a827-dca0a81d5b3a_achizitiidirecte2019t3.xlsx` |
| 2019 | T4 | direct | XLSX | 772 519 | 21 | 226.82 | 123.55 | `1a31ba74-6368-4cc5-8d43-5ca04bdc43a8_achizitiidirecte2019t4.xlsx` |
| 2018 | T1 | contracts | CSV | 23 328 | 39 | 52.59 | 2.39 | `f80fedce-a6b2-4804-9aa8-ad709835bc37_contracte-2018-t1.csv` |
| 2018 | T2 | contracts | XLSX | 5 790 | 36 | 5.13 | 0.41 | `0512843f-f82e-44ee-b2c3-000348414adf_raport-t-2-2018.xls` |
| 2018 | T3 | contracts | XLSX | 10 767 | 36 | 19.05 | 2.15 | `71db8c52-2540-4faf-932c-41f94654b48c_raport-t-3-2018.xls` |
| 2018 | T4 | contracts | XLSX | 11 892 | 36 | 23.52 | 2.60 | `0b2a099f-5ab7-4ebf-89e6-ad8f70b4a637_raport-t-4-2018.xls` |
| 2018 | T1 | contracts_subsequent | CSV | 17 991 | 36 | 46.86 | 1.79 | `74e9eac9-2296-47c5-8978-82e63da74fb0_contractesubsecvente-2018-t1.csv` |
| 2017 | T1 | contracts | CSV | 21 616 | 39 | 45.45 | 1.85 | `b5557679-0331-46e4-b275-e91cb00c4f9c_contracte-2017-t1.csv` |
| 2017 | T2 | contracts | CSV | 32 277 | 39 | 64.76 | 2.75 | `33d0caec-dc1b-41af-8cea-4f7018edf7d3_contracte-2017-t2.csv` |
| 2017 | T3 | contracts | CSV | 32 441 | 39 | 59.80 | 3.20 | `9c8bf3c6-8193-4b3c-88a0-4398ca9132c1_contracte-2017-t3.csv` |
| 2017 | T4 | contracts | CSV | 15 715 | 39 | 29.49 | 1.87 | `207bb4ae-fd4e-46f7-aee7-a670dcf36057_contracte-2017-t4.csv` |
| 2017 | T1 | contracts_subsequent | CSV | 11 405 | 36 | 29.76 | 1.13 | `9ef1d77f-0813-475d-817d-4e723644e4c4_contracte-subsecvente-2017-t1.csv` |
| 2017 | T2 | contracts_subsequent | CSV | 12 874 | 36 | 33.51 | 1.19 | `25627fe3-2c56-444a-b22f-b2e19177a94e_contracte-subsecvente-2017-t2.csv` |
| 2017 | T3 | contracts_subsequent | CSV | 11 855 | 36 | 29.75 | 1.43 | `3cc76965-8f4c-4498-b8ef-48db08fee8da_contracte-subsecvente-2017-t3.csv` |
| 2017 | T4 | contracts_subsequent | CSV | 5 844 | 36 | 14.87 | 0.92 | `df280754-e4c8-4b41-99fa-e8cc1dc92210_contracte-subsecvente-2017-t4.csv` |
| 2016 | S1 | contracts | CSV | 39 811 | 39 | 79.28 | 4.41 | `b41e3020-66af-435a-8acb-2447886d9065_contracte-2016-s1.csv` |
| 2016 | S2 | contracts | CSV | 35 557 | 39 | 72.15 | 3.94 | `9a15e52f-f06d-4e35-aa5b-9e5c6a33a0c2_contracte-2016-s2.csv` |
| 2016 | S1 | contracts_subsequent | CSV | 23 544 | 39 | 59.90 | 4.44 | `37a5429a-891f-470c-8e97-87d1d835a5fa_contracte-subsecvente-2016-s1.csv` |
| 2016 | S2 | contracts_subsequent | CSV | 21 936 | 39 | 57.50 | 4.18 | `427b3e4c-838a-48f9-874a-40fb29034d08_contracte-subsecvente-2016-s2.csv` |
| 2007 | anual | contracts | CSV | 62 220 | 39 | 38.14 | 5.98 | `c6abc0ef-3efb-4aef-bc0a-411f8cab2a28_contracte-2007.csv` |
| 2012 | S1 | contracts | CSV | 47 077 | 39 | 48.52 | 2.86 | `432b8b75-eced-44d8-b32f-3dcb4f368be7_contrace-2012-s1.csv` |
| 2012 | S2 | contracts | CSV | 60 961 | 39 | 91.32 | 4.58 | `91494a89-2383-4f4b-8097-fcb99ebffc18_contracte-2012-s2.csv` |
| 2008 | anual | contracts | CSV | 114 602 | 39 | 65.70 | 10.25 | `2008_7ae7f6d5-fa9a-42aa-9cae-4f71f64ce451_contracte-2008.csv` |
| 2009 | anual | contracts | CSV | 122 353 | 39 | 69.76 | 7.63 | `2009_6a9ba0f2-6fe3-4da4-ae20-c0e97de83230_contracte-2009.csv` |
| 2010 | anual | contracts | CSV | 124 347 | 39 | 73.72 | 6.92 | `2010_e7ef4edc-309a-47ca-9e8b-be3986507752_contracte-2010.csv` |
| 2011 | anual | contracts | CSV | 105 688 | 39 | 67.17 | 5.85 | `2011_842622dd-936c-494c-b992-49187b49e238_contracte-2011.csv` |
| 2013 | S1 | contracts | CSV | 28 512 | 39 | 40.77 | 4.23 | `2013_99f8d3bb-9a16-43e3-9157-f4eeec119584_contracte-2013-s1.csv` |
| 2013 | S2 | contracts | CSV | 38 132 | 39 | 72.33 | 5.91 | `2013_fec15757-02aa-42b1-8524-37da8fd14480_contracte-2013-s2.csv` |
| 2014 | S1 | contracts | CSV | 33 250 | 39 | 64.56 | 4.58 | `2014_cfe94ff9-e85e-4991-86ba-22ea376bcc67_contracte-2014-s1.csv` |
| 2014 | S2 | contracts | CSV | 40 577 | 39 | 78.41 | 6.57 | `2014_9e243b07-1a11-4052-8beb-8fdef730df8d_contracte-2014-s2.csv` |
| 2015 | S1 | contracts | CSV | 36 808 | 39 | 69.94 | 5.72 | `2015_53673c9f-04b7-4b54-bf40-9db868afdaa5_contracte-2015-s1.csv` |
| 2015 | S2 | contracts | CSV | 40 291 | 39 | 78.30 | 5.53 | `2015_fa5d8e71-8f87-4775-a8a8-fe0bb23f7b1c_contracte-2015-s2.csv` |

## Fișiere locale și reproducere

- Fișiere originale: `data/raw/{year}/` și `data/raw/historical/`.
- Tabele Parquet: `data/processed/{type}/year=YYYY/quarter={t1..t4,s1,s2,annual}.parquet`.
- Raport automat de import: `data/processed/import_report.json`.
- Proveniență/URL-uri/licențe: `data/source_manifest.json`.
- Cod: `scripts/download_data.py`, `scripts/import_data.py`; instalare din `requirements.txt`.
- Datele brute și procesate sunt ignorate de Git; repository-ul conține cod, manifest și documentație.

## Pași următori

1. Dicționar de antete canonice și standardizarea separată a achizițiilor directe, contractelor și subsecventelor.
2. Conversie controlată pentru date, valori, monede, CUI și CPV; păstrarea câmpurilor originale și a provenienței.
3. Profilarea duplicatelor, lipsurilor, codărilor și valorilor extreme pe fiecare an/sursă.
4. Măsurarea suprapunerii între exporturile naționale și pachetele tematice/instituționale înainte de unire.
5. Abia apoi agregări comparative și analize de furnizori, autorități, CPV și proceduri.
