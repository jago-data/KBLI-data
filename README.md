# KBLI-data

KBLI 2025 (Klasifikasi Baku Lapangan Usaha Indonesia) dataset scraped from
[legalitas.org/kbli](https://legalitas.org/kbli).

## Contents

| File | Description |
|---|---|
| `kbli_2025_legalitas.xlsx` | Complete dataset — 1,520 five-digit KBLI codes (`01111` – `99000`) |
| `scrape_kbli.py` | Scraper script (Python + Polars) |

## Columns

| Column | Description |
|---|---|
| **Kode KBLI** | 5-digit KBLI code (stored as text, leading zeros preserved) |
| **Judul** | Business classification title |
| **Uraian** | Full description of the classification |
| **Level** | Classification level (all rows are "Kelompok") |

## How it works

The scraper hits the site's DataTables AJAX endpoint
(`https://legalitas.org/kbli/ajax`), which returns the entire dataset in a
single JSON response — the same source the website's interactive table loads.
It then validates the data (unique codes, 5-digit format, no empty fields)
and exports to XLSX.

## Re-running

```bash
pip install polars xlsxwriter
python3 scrape_kbli.py
```
