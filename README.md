# IIVR-SP — São Paulo Repeat-Sales Housing Index

A repeat-sales house price index (Case-Shiller method) for the city of São Paulo,
built from ITBI property-transfer-tax microdata and benchmarked against IPCA, CDI,
FipeZAP and the Ibovespa (2010–2025).

**Live page:** https://otaviolmbraga.github.io/sp-housing-index/

This repository is the **public front-end only**: a single interactive page plus
the small index series and a few PDFs. The analysis code and raw data live in a
separate private repository.

## Contents

| Path | What it is |
|------|------------|
| `index.html` | The interactive page (PT/EN, comparison chart, returns table). Open it by double-clicking, or serve via GitHub Pages. |
| `data.js` | The monthly index series embedded for the page (`window.CS_DATA`). Auto-generated. |
| `data/ivr_sp_index.csv` | The monthly IIVR-SP index series (levels + 12-month change) and benchmarks, 2010–2025. Committed for direct download/citation. |
| `docs/` | Comments (EN), methodology note PDFs, and the bilingual data dictionary. |
| `og-image.png` | Social-share preview card (Open Graph / Twitter). |
| `_build/make_site_data.py` | Regenerates `data.js` and the compressed transaction download. Not needed to view the site. |
| `_release_assets/` | Local-only; the compressed transaction CSV staged for upload to a GitHub Release (git-ignored). |

## Transaction microdata

The full transaction dataset is large and is **not** stored in this repo. It is
attached as a compressed asset (`itbi_compilado.csv.gz`, ~192 MB) to the latest
[GitHub Release](../../releases/latest). Read it in Python with:

```python
import pandas as pd
df = pd.read_csv("itbi_compilado.csv.gz")   # pandas decompresses .gz automatically
```

## Regenerating the data

```bash
python _build/make_site_data.py
```

This reads the clean index CSV and the transaction CSV from the private analysis
folder and writes `data.js`, `data/ivr_sp_index.csv`, and
`_release_assets/itbi_compilado.csv.gz`.

## Data dictionary

See [`docs/data_dictionary.md`](docs/data_dictionary.md) for a bilingual (EN/PT)
description of every column in the transaction microdata.

## How to cite

> Braga, Otávio. *IIVR-SP — São Paulo Repeat-Sales Housing Index.*
> https://otaviolmbraga.github.io/sp-housing-index/

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff).

## License

- **Data and documents** (index series, transaction microdata, PDFs): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- **Website code** (`index.html`, `data.js`, `_build/`): MIT.

See [`LICENSE`](LICENSE) for details.
