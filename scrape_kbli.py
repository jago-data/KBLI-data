"""Scrape KBLI 2025 data from https://legalitas.org/kbli and export to XLSX."""
import json
import urllib.request

import polars as pl

URL = "https://legalitas.org/kbli/ajax"
OUTPUT = "kbli_2025_legalitas.xlsx"

req = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "X-Requested-With": "XMLHttpRequest",
    },
)
with urllib.request.urlopen(req) as resp:
    payload = json.load(resp)

rows = payload["data"]
print(f"Fetched {len(rows)} rows")

df = (
    pl.DataFrame(rows)
    .select(
        pl.col("kode").alias("Kode KBLI"),
        pl.col("judul").alias("Judul"),
        pl.col("uraian").alias("Uraian"),
        pl.col("level").alias("Level"),
    )
    .sort("Kode KBLI")
)

# Sanity checks: all codes unique, 5-digit, non-empty descriptions
assert df["Kode KBLI"].n_unique() == len(df), "duplicate KBLI codes found"
assert (df["Kode KBLI"].str.len_chars() == 5).all(), "non 5-digit code found"
print(f"Unique codes: {df['Kode KBLI'].n_unique()}")
print(f"Empty judul: {(df['Judul'].is_null() | (df['Judul'] == '')).sum()}")
print(f"Empty uraian: {(df['Uraian'].is_null() | (df['Uraian'] == '')).sum()}")

df.write_excel(
    OUTPUT,
    worksheet="KBLI 2025",
    autofit=True,
    header_format={"bold": True, "bg_color": "#1F4E78", "font_color": "white"},
    column_widths={"Uraian": 120},
    freeze_panes=(1, 0),
)
print(f"Saved {OUTPUT}")
