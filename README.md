# CodexVitae

CodexVitae is a small non-profit that maintains the Sardinia Endemism Atlas, with about 1,500 endemic species and subspecies of Sardinia and Corsica. We have a MinION sequencer and collaborate with the University of Milan on molecular biology. We barcode field samples and some public and private collections.

- Website: https://www.codexvitae.it/
- Atlas: https://www.codexvitae.it/atlante/

The figure of about 1,500 is the scope of the atlas on the website. This repository contains a CSV of endemic names and flora links, a Python script that looks up missing Acta Plantarum links, and the pinned Python dependencies for that script.

## Repository contents

| Path | What it is |
| --- | --- |
| `dati/endemismi.csv` | Comma-separated table of endemic taxa and flora links (249 data rows) |
| `acta-plantarum-updater.py` | Reads `endemismi.csv` from the current directory, looks up Acta Plantarum, and writes `endemismi_updated.csv` |
| `requirements.txt` | Pinned Python packages |
| `.gitattributes` | Git text detection and LF normalization (`* text=auto`) |

## Columns in `dati/endemismi.csv`

The header row is:

```text
ID,Name,SardegnaFlora,Wikiplantbase,FloraItalia,ActaPlantarum,,
```

| Column | What the cells contain |
| --- | --- |
| `ID` | Integer identifier. The 249 values are unique. |
| `Name` | Scientific name. A value may include an infraspecific rank (`subsp.` or `var.`) and may include an author citation. |
| `SardegnaFlora` | A URL, or the literal token `\N`. |
| `Wikiplantbase` | A URL, or `\N`. |
| `FloraItalia` | A URL, or `\N`. |
| `ActaPlantarum` | A URL on `www.actaplantarum.org`, or `\N`. |
| *(empty header)* | Empty in the file, except one cell that contains `\N`. pandas 2.1.4 (the version pinned in `requirements.txt`) names this column `Unnamed: 6`. |
| *(empty header)* | Same pattern as the previous column. pandas 2.1.4 names it `Unnamed: 7`. |

`\N` is stored as two characters. It is not an empty field. In one row, `SardegnaFlora` and `Wikiplantbase` contain a quoted fragment of an author citation, with a leading space, instead of a URL. Names in the table are not limited to plants.

The script reads `Name` and `ActaPlantarum`. The other columns are carried into the output file with the rest of the table.

## What the script does

`acta-plantarum-updater.py` takes no command-line arguments. When run, it loads `endemismi.csv` with `pandas.read_csv`. For each row where `ActaPlantarum` is missing (`pandas.isna`), it does the following:

1. Cleans `Name` for the query. It removes the rank tokens `var.` and `subsp.` and leaves the word that follows. It then keeps the text before the first comma.
2. Percent-encodes that string and requests `https://www.actaplantarum.org/flora/flora_info.php?id=&nnn=` followed by the encoded name.
3. If the HTTP status is 200 and the HTML contains a `div` with class `scheda`, it writes that same request URL into `ActaPlantarum`. The stored URL is the search URL (`id` is empty). The script does not copy a numeric taxon id from the page.
4. Waits 2 seconds before the next row it checks.

If the request fails, the script prints an error and leaves the cell unchanged. Rows that already have an `ActaPlantarum` value are left unchanged. It then writes the whole table to `endemismi_updated.csv` in the current directory, without the dataframe index. The input file is left unchanged.

## Install and run

```bash
python -m pip install -r requirements.txt
python acta-plantarum-updater.py
```

The script imports `pandas`, `requests`, and `BeautifulSoup` from `beautifulsoup4`, and it parses HTML with the Python `html.parser`. `requirements.txt` also pins `lxml`, `numpy`, `python-dotenv`, and `pytest`.

### Note on paths

The script reads `endemismi.csv` and writes `endemismi_updated.csv` in the current working directory. In this repository the table is `dati/endemismi.csv`.

From the repository root, `python acta-plantarum-updater.py` raises `FileNotFoundError` because `endemismi.csv` is not in that directory. To run the script on the checked-in table, start it from `dati`:

```bash
cd dati
python ../acta-plantarum-updater.py
```

The written file is then `dati/endemismi_updated.csv`. The script’s paths and the location of the checked-in table differ; the commands above are the way to line them up.

### Note on `\N`

In `dati/endemismi.csv`, every empty `ActaPlantarum` cell is the token `\N`. pandas 2.1.4 does not treat `\N` as a missing value, so `pandas.isna` is false for all 249 rows. A run against this file sends no requests and leaves every `\N` in place. It still writes `endemismi_updated.csv`. The cell values match the input. The written header names the two blank columns `Unnamed: 6` and `Unnamed: 7`.

The script fills `ActaPlantarum` when that cell is empty in the sense pandas uses for a blank field.

## License

This repository does not include a license file.

## Italiano

CodexVitae è una piccola organizzazione non profit che mantiene il Sardinia Endemism Atlas, con circa 1.500 specie e sottospecie endemiche di Sardegna e Corsica. Abbiamo un sequenziatore MinION e collaboriamo con l’Università di Milano sulla biologia molecolare. Facciamo il barcoding di campioni di campo e di alcune collezioni pubbliche e private.

- Sito: https://www.codexvitae.it/
- Atlante: https://www.codexvitae.it/atlante/

Il repository contiene `dati/endemismi.csv` (249 righe; colonne ID, Name, SardegnaFlora, Wikiplantbase, FloraItalia, ActaPlantarum e due colonne senza intestazione), lo script `acta-plantarum-updater.py` e `requirements.txt`. Lo script legge `endemismi.csv` nella cartella di lavoro e scrive `endemismi_updated.csv`. Il CSV è in `dati/`, e i link assenti sono il testo `\N`, che lo script non considera mancante. Installazione, comportamento dello script e note sono nella parte in inglese.
