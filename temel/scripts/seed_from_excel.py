"""
Seed companies from temelozet.xlsx into D1-compatible SQL
Usage: python scripts/seed_from_excel.py
Output: db/seed_companies.sql (for D1 import)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd

EXCEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'temelozet.xlsx')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'src', 'db', 'seed_companies.sql')

def financial_group_for_sector(sector):
    sector = sector.strip().lower()
    if any(k in sector for k in ['bankacılık', 'finans', 'fin.', 'faktoring']):
        return 'UFRS_K'
    if any(k in sector for k in ['sigorta']):
        return 'UFRS_S'
    if sector == 'gyo':
        return 'UFRS_K'
    return 'XI_29'

def main():
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    sql_lines = [
        "-- Seed companies from temelozet.xlsx",
        "-- Generated automatically, do not edit manually",
        "",
        "INSERT OR REPLACE INTO companies (ticker, name, sector_raw, sector_main, financial_group, market_cap, shares_outstanding, free_float_pct) VALUES"
    ]

    values = []
    for _, row in df.iterrows():
        ticker = str(row.get('Kod', '')).strip().upper()
        name = str(row.get('Hisse Adı', row.get('Hisse Ad�', ''))).strip().replace("'", "''")
        sector = str(row.get('Sektör', row.get('Sekt�r', ''))).strip().replace("'", "''")
        price = row.get('Kapanış(TL)', row.get('Kapan��(TL)', 0))
        mcap_tl = row.get('Piyasa Değeri(mn TL)', row.get('Piyasa De�eri(mn TL)', 0))
        ff_pct = row.get('Halka AçıklıkOranı (%)', row.get('Halka A��kl�kOran� (%)', 0))
        shares = row.get('Sermaye(mn TL)', 0)

        if pd.isna(ticker) or not ticker:
            continue

        mcap = int(float(mcap_tl) * 1_000_000) if not pd.isna(mcap_tl) else 0
        shares_val = int(float(shares) * 1_000_000) if not pd.isna(shares) else 0
        ff = float(ff_pct) if not pd.isna(ff_pct) else None
        fin_group = financial_group_for_sector(sector)

        vals = f"('{ticker}', '{name}', '{sector}', '{sector}', '{fin_group}', {mcap}, {shares_val}, {ff if ff is not None else 'NULL'})"
        values.append(vals)

    sql_lines.append(",\n".join(values) + ";")
    sql_lines.append("")
    sql_lines.append("CREATE INDEX IF NOT EXISTS idx_companies_sector ON companies(sector_main);")
    sql_lines.append("CREATE INDEX IF NOT EXISTS idx_companies_active ON companies(is_active);")

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(sql_lines))

    print(f"✅ Generated {len(values)} companies → {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
