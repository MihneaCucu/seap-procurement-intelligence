# Propunere de dataset: achiziții publice SEAP din România, 2007–2025

## 1. De ce acest dataset?

Construim un dataset derivat din exporturile oficiale SEAP publicate pe data.gov.ro, care reunește date despre achiziții publice din mai mulți ani și propune o schemă comună. Sursele existente oferă informațiile de bază, dar sunt publicate în fișiere separate, cu structuri, denumiri de coloane și formate diferite. Datasetul nostru urmărește să faciliteze căutarea, compararea și analiza lor în timp, păstrând proveniența fiecărei înregistrări. Ar putea fi folosit de jurnaliști, organizații civice, cercetători și firme care urmăresc piața, pentru a explora achizițiile după autoritate, obiect/CPV, tip și valoare.

Importul curent conține **20.412.240 de rânduri din 86 de resurse**: 16.224.190 achiziții directe, 4.082.601 contracte publicate și 105.449 contracte subsecvente. Nu am deduplicat, deci numărul rândurilor nu trebuie interpretat ca număr de achiziții economice unice. Fișierele au fost parsate în Parquet, dar câmpurile și valorile nu sunt încă armonizate: coloanele diferă în funcție de an și tip, iar valorile importate sunt păstrate ca text.

## 2. Surse și acoperire

Prima versiune folosește exclusiv portalul oficial [data.gov.ro](https://data.gov.ro/), prin 11 pachete, inclusiv [Achiziții publice 2025](https://data.gov.ro/dataset/achizitii-publice-2025), [2023](https://data.gov.ro/dataset/achizitii-publice-2023), [2016](https://data.gov.ro/dataset/achizitii-publice-2016) și [contracte istorice 2007–2015](https://data.gov.ro/dataset/achizitii-publice-2007-2016-contracte6). Resursele însumează aproximativ **7,67 GB în formatele publicate** și **1,59 GB în Parquet-ul rezultat**. Licențele declarate în portal sunt **CC BY 4.0** pentru pachetele 2021–2025 și **OGL-ROU-1.0** pentru pachetele mai vechi. Lista resurselor, URL-urile și licențele folosite sunt consemnate în [manifestul surselor](../data/source_manifest.json).

| Perioadă | Date importate | Granularitatea exporturilor |
|---|---|---|
| 2007–2011 | Contracte publicate | anual |
| 2012–2015 | Contracte publicate | semestre |
| 2016 | Contracte și contracte subsecvente | semestre |
| 2017 | Contracte și contracte subsecvente | trimestre |
| 2018 | Contracte trimestriale; contracte subsecvente pentru T1 | trimestre, acoperire incompletă la subsecvente |
| 2019–2025 | Contracte publicate și achiziții directe | trimestre |

În continuarea proiectului vom căuta și integra, pe cât posibil, surse românești suplimentare: exporturi din e-licitatie.ro, date OpenTender relevante pentru România, nomenclatorul CPV și cursurile BNR. Le vom evalua și documenta separat înainte de includere. Vom urmări să completăm câmpurile pentru județ, numărul de oferte și valorile în EUR, precum și să verificăm forma juridică a furnizorilor. Aceste informații nu sunt uniforme în importul actual și vor fi completate numai după identificarea și validarea surselor sau a regulilor potrivite.

## 3. Date cu caracter personal

Exporturile pot conține date personale: nume și identificatori ai unor furnizori persoane fizice sau PFA, adrese și informații de contact, precum și date introduse în descrieri libere. Nu am identificat încă toate persoanele fizice și nu am verificat integral textele.

Înainte de publicarea datelor prelucrate, vom verifica tipul furnizorilor și vom elimina numele și identificatorii celor detectați ca persoane fizice sau PFA; când nu putem stabili tipul furnizorului, vom omite câmpurile care îl pot identifica. Vom elimina adresele și datele de contact personale, vom verifica descrierile și vom redacta informațiile personale găsite sau vom exclude înregistrările care nu pot fi curățate în siguranță. Eșantionul actual nu conține numele sau CUI-urile furnizorilor și nici CUI-urile autorităților. Am revizuit vizual câmpurile text din cele 32 de rânduri și nu am identificat date de contact sau identificatori ai persoanelor fizice.

## 4. Schema comună pentru setul final

O înregistrare reprezintă un rând dintr-un export de achiziție directă, contract sau contract subsecvent. Schema de mai jos este **schema țintă** a setului final: câmpurile opționale pot lipsi când sursa nu le furnizează sau când trebuie protejate datele personale. Importul actual nu este încă transformat integral în această schemă.

| Câmp | Tip | Ce reprezintă |
|---|---|---|
| `source_year` | integer | Anul exportului |
| `source_period` | string | Perioada exportului: `annual`, `s1`, `s2`, `t1`–`t4` |
| `record_type` | enum | `direct_purchase`, `published_contract` sau `subsequent_contract` |
| `contracting_authority` | string, opțional | Autoritatea contractantă |
| `authority_county` | string, opțional | Județul autorității, dacă este verificat |
| `procurement_reference` | string, opțional | Numărul achiziției, anunțului sau contractului |
| `published_at` | string, opțional | Data publicării disponibilă în sursă |
| `contract_or_completion_date` | string, opțional | Data contractului sau a finalizării, după tipul exportului |
| `title` | string, opțional | Titlul sau denumirea achiziției |
| `cpv_code` | string, opțional | Codul CPV |
| `cpv_label` | string, opțional | Denumirea categoriei CPV |
| `contract_type` | string, opțional | Tipul contractului |
| `procedure_type` | string, opțional | Tipul procedurii, unde este disponibil |
| `number_of_offers` | integer, opțional | Numărul de oferte, unde este disponibil |
| `supplier_name` | string, opțional | Numele furnizorului, după verificarea datelor personale |
| `supplier_identifier` | string, opțional | Identificatorul furnizorului, după verificarea datelor personale |
| `amount_source` | string, opțional | Valoarea achiziției sau contractului din export; nu este neapărat preț unitar sau suma plătită |
| `currency_source` | string, opțional | Moneda valorii din export |
| `amount_eur` | decimal, opțional | Valoarea în EUR, când conversia a fost validată |
| `quantity` | decimal, opțional | Cantitatea, dacă este disponibilă și verificată |
| `quantity_unit` | string, opțional | Unitatea de măsură, dacă este disponibilă |
| `source_resource_id` | string | Identificatorul resursei de origine |
| `source_file` | string | Numele fișierului de origine |

Cantitatea, unitatea și valoarea convertită în EUR nu au fost completate în eșantion. Câmpurile furnizorilor sunt goale în eșantion; eventualele date publicate vor respecta măsurile descrise în secțiunea 3. Datele și valorile din export nu au fost încă normalizate.

Exemplele sunt fragmente din rândurile reale ale eșantionului. Câmpurile lipsă din exemple sunt opționale; datele de proveniență sunt incluse. În eșantion, tipurile înregistrărilor sunt redenumite conform schemei comune.

```jsonl
{"source_year":2007,"source_period":"annual","record_type":"published_contract","contracting_authority":"MINISTERUL APARARII UM 02534 IASI","procurement_reference":"A/1605/1","title":"CONTRACT FURNIZARE REACTIVI","cpv_code":"24496500-2","amount_source":"1568.50","currency_source":"RON","source_resource_id":"c6abc0ef-3efb-4aef-bc0a-411f8cab2a28","source_file":"c6abc0ef-3efb-4aef-bc0a-411f8cab2a28_contracte-2007.csv"}
{"source_year":2016,"source_period":"s1","record_type":"subsequent_contract","contracting_authority":"ENEL DISTRIBUTIE BANAT SA Timisoara","procurement_reference":"CS 1-AC 572 EDB","title":"MENTENANTA INSTALATII MT-JT ZONA RESITA EDB","cpv_code":"45315500-3","amount_source":"1727061.4700","currency_source":"RON","source_resource_id":"37a5429a-891f-470c-8e97-87d1d835a5fa","source_file":"37a5429a-891f-470c-8e97-87d1d835a5fa_contracte-subsecvente-2016-s1.csv"}
{"source_year":2020,"source_period":"t1","record_type":"direct_purchase","contracting_authority":"Spital General CF Sibiu","procurement_reference":"DA25231029","title":"Achizitie aparat aerosoli","cpv_code":"24959100-2","amount_source":"137","currency_source":"RON","source_resource_id":"3e827637-6aba-4b47-85c9-e09f05c71057","source_file":"3e827637-6aba-4b47-85c9-e09f05c71057_achizitii_directe_2020_t1.xlsx"}
```

Perioada exportului nu este neapărat anul evenimentului: de exemplu, unele contracte publicate în exporturi recente au date de contract din ani anteriori. Schema păstrează separat anul/perioada sursei și datele din rând, atunci când sunt disponibile.

## 5. Cum demonstrăm utilitatea?

La final, ne propunem să demonstrăm că datasetul poate susține următoarele analize și modele, în funcție de calitatea și disponibilitatea datelor:

- **Predicția prețurilor:** estimarea valorii unor achiziții comparabile, pornind de la caracteristicile disponibile.
- **Detectarea anomaliilor:** identificarea valorilor neobișnuite pentru achiziții comparabile.
- **Estimarea cheltuielilor:** prognoza cheltuielilor viitoare pe categorii sau instituții, folosind serii istorice.
- **Analiza furnizorilor:** explorarea relațiilor dintre instituții și firmele câștigătoare, inclusiv prin grafuri.
- **Clasificarea produselor și serviciilor:** clasificarea automată a descrierilor, de exemplu după categorii CPV.

O extensie a analizei furnizorilor este investigarea legăturilor dintre firmele câștigătoare și persoane cu funcții publice, folosind surse suplimentare verificate. O legătură sau o valoare neobișnuită indică necesitatea unei verificări, dar nu dovedește existența unei nereguli. Pentru predicții și comparații de preț, vom evalua dacă există suficiente informații despre cantități și caracteristicile achizițiilor.

Pentru a arăta utilitatea la final, vom realiza cel puțin o analiză pe datele armonizate și îi vom evalua rezultatele față de un reper potrivit; de exemplu, pentru detectarea anomaliilor, vom verifica manual un eșantion de achiziții semnalate.

[Eșantionul CSV](data-sample.csv) atașat are **32 de rânduri reale**, câte 8 din fiecare dintre patru extrase: contracte din 2007, contracte subsecvente din 2016, achiziții directe din 2020 și contracte publicate din 2025. Include 32 de autorități și 31 de coduri CPV distincte.
