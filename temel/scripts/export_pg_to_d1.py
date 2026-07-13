"""
PostgreSQL → D1 SQL Export Script
Reads data from old PostgreSQL and generates INSERT OR REPLACE SQL files for D1.
"""
import psycopg2
import os
from datetime import datetime

DB_CONFIG = {
    "host": "postgresql-77b1bcb9-o033531ff.database.cloud.ovh.net",
    "port": 20184,
    "user": "avnadmin",
    "password": "H3m7baA6K5Ix1NoLWGsM",
    "dbname": "compengine",
    "sslmode": "require"
}

OUTPUT_DIR = "seed_output"
BATCH_SIZE = 500


def clean_value(val):
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "1" if val else "0"
    from decimal import Decimal
    if isinstance(val, Decimal):
        return str(float(val))
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, datetime):
        return f"'{val.isoformat()}'"
    s = str(val).replace("'", "''")
    return f"'{s}'"


def export_table(cur, table, columns, query, output_file):
    cur.execute(query)
    rows = cur.fetchall()
    total = len(rows)
    print(f"{table}: {total} rows")

    col_names = [c.split(".")[-1] if "." in c else c for c in columns]
    col_list = ", ".join(col_names)
    col_placeholders = ", ".join([f"'{c}'" for c in col_names])

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"-- {table}: {total} rows (exported {datetime.utcnow().isoformat()})\n")
        f.write(f"INSERT OR REPLACE INTO {table} ({col_list}) VALUES\n")
        batch = []
        row_count = 0
        for row in rows:
            vals = ", ".join(clean_value(v) for v in row)
            batch.append(f"({vals})")
            row_count += 1
            if len(batch) >= BATCH_SIZE:
                f.write(",\n".join(batch))
                f.write(";\n\n")
                f.write(f"INSERT OR REPLACE INTO {table} ({col_list}) VALUES\n")
                batch = []
        if batch:
            f.write(",\n".join(batch))
            f.write(";\n")
        else:
            f.seek(f.tell() - len(f"\nINSERT OR REPLACE INTO {table} ({col_list}) VALUES\n"))
            f.truncate()

    print(f"  → {output_file}")
    return total


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    total_rows = 0

    # 1. financial_statements_raw (332K rows)
    cols = ["ticker", "period_key", "year", "period", "financial_group",
            "item_code", "item_desc_tr", "item_desc_en", "value_try", "fetched_at"]
    total_rows += export_table(
        cur,
        "financial_statements_raw",
        cols,
        "SELECT ticker, period_key, year, period, financial_group, item_code, item_desc_tr, item_desc_en, value_try, fetched_at FROM financial_statements_raw ORDER BY ticker, period_key, item_code",
        os.path.join(OUTPUT_DIR, "seed_statements.sql")
    )

    # 2. company_metrics (609 rows)
    cols = ["ticker", "last_price", "market_cap", "shares_outstanding", "free_float_pct",
            "volume_1d", "volume_avg_30d", "pe_ratio", "pb_ratio", "price_updated_at"]
    total_rows += export_table(
        cur,
        "company_metrics",
        cols,
        "SELECT ticker, last_price, market_cap, shares_outstanding, free_float_pct, volume_1d, volume_avg_30d, pe_ratio, pb_ratio, price_updated_at FROM company_metrics ORDER BY ticker",
        os.path.join(OUTPUT_DIR, "seed_metrics.sql")
    )

    # 3. company_ratios (23K rows) — optional, saves recalculation
    cols = ["ticker", "period_key", "ratio_code", "ratio_value", "is_ttm",
            "calculation_method", "data_quality_score", "computed_at"]
    total_rows += export_table(
        cur,
        "company_ratios",
        cols,
        "SELECT ticker, period_key, ratio_code, ratio_value, CAST(is_ttm AS INTEGER), calculation_method, data_quality_score, computed_at FROM company_ratios ORDER BY ticker, period_key, ratio_code",
        os.path.join(OUTPUT_DIR, "seed_ratios.sql")
    )

    # 4. company_scores (1.1K rows) — phase 2, but nice to have
    cols = ["ticker", "period_key", "score_sektor", "score_genel",
            "score_karlilik", "score_finansal", "score_verimlilik", "score_degerleme",
            "reliability_score", "data_quality_score", "computed_at"]
    # Check if company_scores exists
    try:
        cur.execute("SELECT EXISTS(SELECT FROM information_schema.tables WHERE table_name = 'company_scores')")
        if cur.fetchone()[0]:
            total_rows += export_table(
                cur,
                "company_scores",
                cols,
                "SELECT ticker, period_key, score_sektor, score_genel, score_karlilik, score_finansal, score_verimlilik, score_degerleme, reliability_score, data_quality_score, computed_at FROM company_scores ORDER BY ticker, period_key",
                os.path.join(OUTPUT_DIR, "seed_scores.sql")
            )
    except Exception:
        pass

    # 4. item_code_mappings (130 rows)
    cols = ["financial_group", "item_code", "semantic_name", "description_tr",
            "description_en", "statement_type", "category", "is_primary", "priority"]
    total_rows += export_table(
        cur,
        "item_code_mappings",
        cols,
        "SELECT financial_group, item_code, semantic_name, description_tr, description_en, statement_type, category, CAST(is_primary AS INTEGER), priority FROM item_code_mappings ORDER BY financial_group, item_code",
        os.path.join(OUTPUT_DIR, "seed_item_codes.sql")
    )

    cur.close()
    conn.close()
    print(f"\n✅ Export complete: {total_rows} rows across {len(os.listdir(OUTPUT_DIR))} files")


if __name__ == "__main__":
    main()
