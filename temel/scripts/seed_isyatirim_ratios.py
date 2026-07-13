import openpyxl
from datetime import datetime

BASE = r"C:\Users\ASUS\hp\comp\is-yatirim-temel"
OUT = r"C:\Users\ASUS\hp\comp\seed_output"
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def tr_lower(s):
    if not s:
        return ""
    result = []
    for c in s:
        if c == '\u0130':
            result.append('i')
        elif c == '\u0131':
            result.append('i')
        elif c == '\u015e' or c == '\u015f':
            result.append('s')
        elif c == '\u00c7' or c == '\u00e7':
            result.append('c')
        elif c == '\u00dc' or c == '\u00fc':
            result.append('u')
        elif c == '\u00d6' or c == '\u00f6':
            result.append('o')
        elif c == '\u011e' or c == '\u011f':
            result.append('g')
        else:
            result.append(c.lower())
    return "".join(result)


def parse_ad(val):
    if val is None:
        return None
    s = str(val).strip()
    if s.upper() in ("A/D", "AD", "N/A", "", "NONE"):
        return None
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


def sql_val(v):
    if v is None:
        return "NULL"
    if isinstance(v, (float, int)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def read_xlsx(filename, sheet="isyatirim"):
    wb = openpyxl.load_workbook(f"{BASE}/{filename}", data_only=True)
    ws = wb[sheet]
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        rows.append(row)
    return rows


ozet_rows = read_xlsx("temelozet.xlsx")
finansal_rows = read_xlsx("temelfinansal.xlsx")
sermaye_rows = read_xlsx("temelsermaye.xlsx")
tarihsel_rows = read_xlsx("temeltarihsel.xlsx")

ozet = {}
for r in ozet_rows:
    ticker = str(r[0]).strip() if r[0] else None
    if not ticker:
        continue
    ozet[ticker] = {
        "name": str(r[1]).strip() if r[1] else None,
        "sector": str(r[2]).strip() if r[2] else None,
        "last_price": parse_ad(r[3]),
        "market_cap_tl": parse_ad(r[4]),
        "market_cap_usd": parse_ad(r[5]),
        "free_float_pct": parse_ad(r[6]),
        "capital_mn_tl": parse_ad(r[7]),
    }

finansal = {}
for r in finansal_rows:
    ticker = str(r[0]).strip() if r[0] else None
    if not ticker:
        continue
    finansal[ticker] = {
        "last_price": parse_ad(r[1]),
        "pe_ratio": parse_ad(r[2]),
        "ev_ebitda": parse_ad(r[3]),
        "ev_sales": parse_ad(r[4]),
        "pb_ratio": parse_ad(r[5]),
        "last_period": str(r[6]).strip() if r[6] else None,
    }

sermaye = {}
for r in sermaye_rows:
    ticker = str(r[0]).strip() if r[0] else None
    if not ticker:
        continue
    if ticker not in sermaye:
        sermaye[ticker] = []
    sermaye[ticker].append({
        "close": parse_ad(r[1]),
        "post_split_capital": parse_ad(r[2]),
        "date": str(r[3]).strip() if r[3] else None,
        "rights_offering_pct": parse_ad(r[4]),
        "rights_nominal": parse_ad(r[5]),
        "other": parse_ad(r[6]),
        "bonus_internal_pct": parse_ad(r[7]),
        "bonus_dividend_pct": parse_ad(r[8]),
        "cash_dividend_gross_pct": parse_ad(r[9]),
        "cash_dividend_total": parse_ad(r[10]),
        "dividend_per_share": parse_ad(r[11]),
    })

tarihsel = {}
for r in tarihsel_rows:
    ticker = str(r[0]).strip() if r[0] else None
    if not ticker:
        continue
    tarihsel[ticker] = {
        "last_price": parse_ad(r[1]),
        "forward_pe": parse_ad(r[2]),
        "pe_premium_discount": parse_ad(r[3]),
        "forward_ev_ebitda": parse_ad(r[4]),
        "ev_ebitda_premium_discount": parse_ad(r[5]),
        "forward_pb": parse_ad(r[6]),
        "pb_premium_discount": parse_ad(r[7]),
    }

all_tickers = sorted(set(list(ozet.keys()) + list(finansal.keys()) + list(sermaye.keys()) + list(tarihsel.keys())))

ratios_lines = []
metrics_lines = []
profit_lines = []
sector_counts = {}

for ticker in all_tickers:
    o = ozet.get(ticker, {})
    f = finansal.get(ticker, {})
    t = tarihsel.get(ticker, {})

    sector = o.get("sector") if o.get("sector") else None
    last_price = o.get("last_price") or f.get("last_price") or t.get("last_price")
    mc_tl = o.get("market_cap_tl")
    mc_usd = o.get("market_cap_usd")
    ff = o.get("free_float_pct")
    capital = o.get("capital_mn_tl")
    pe = f.get("pe_ratio")
    ev_ebitda = f.get("ev_ebitda")
    ev_sales = f.get("ev_sales")
    pb = f.get("pb_ratio")
    period = f.get("last_period")
    fpe = t.get("forward_pe")
    fev_ebitda = t.get("forward_ev_ebitda")
    fpb = t.get("forward_pb")

    # --- isyatirim_ratios ---
    vals = {
        "ticker": ticker,
        "sector": sector,
        "last_price": last_price,
        "market_cap_tl": mc_tl,
        "market_cap_usd": mc_usd,
        "free_float_pct": ff,
        "capital_mn_tl": capital,
        "pe_ratio": pe,
        "ev_ebitda": ev_ebitda,
        "ev_sales": ev_sales,
        "pb_ratio": pb,
        "forward_pe": fpe,
        "forward_ev_ebitda": fev_ebitda,
        "forward_pb": fpb,
        "last_period": period,
        "data_date": NOW[:10],
    }

    cols = ", ".join(vals.keys())
    vals_str = ", ".join([sql_val(v) for v in vals.values()])
    ratios_lines.append(f"INSERT OR REPLACE INTO isyatirim_ratios ({cols}) VALUES ({vals_str});")

    # --- company_metrics ---
    shares = int(capital * 1_000_000) if capital else None
    mc_int = int(mc_tl * 1_000_000) if mc_tl else None

    metrics_lines.append(
        f"INSERT OR REPLACE INTO company_metrics (ticker, last_price, market_cap, shares_outstanding, free_float_pct, pe_ratio, pb_ratio, price_updated_at) "
        f"VALUES ({sql_val(ticker)}, {sql_val(last_price)}, {sql_val(mc_int)}, {sql_val(shares)}, {sql_val(ff)}, {sql_val(pe)}, {sql_val(pb)}, '{NOW}');"
    )

    # --- company_sector_profiles ---
    sg = "other"
    if sector:
        s_lower = tr_lower(sector)
        if "banka" in s_lower:
            sg = "banking"
        elif "sigorta" in s_lower:
            sg = "insurance"
        elif "gyo" in s_lower or "gayrimenkul" in s_lower:
            sg = "reit"
        elif "holding" in s_lower:
            sg = "holding"
        elif any(x in s_lower for x in ["finansal", "faktoring", "fin.kiralama", "varlik", "yatirim ortak"]):
            sg = "financial"
        elif "araci" in s_lower:
            sg = "brokerage"
        else:
            sg = "industrial"

    has_loans = 1 if sg in ("banking", "financial") else 0
    has_insurance = 1 if sg == "insurance" else 0
    has_inventory = 1 if sg in ("industrial", "reit") else 0
    has_receivables = 1 if sg != "banking" else 0
    is_financial = 1 if sg in ("banking", "financial", "insurance", "brokerage") else 0
    is_holding = 1 if sg == "holding" else 0
    is_reit = 1 if sg == "reit" else 0

    profit_lines.append(
        f"INSERT OR REPLACE INTO company_sector_profiles (ticker, sector_name, sector_group, has_loans, has_insurance, has_inventory, has_receivables, is_financial, is_holding, is_reit) "
        f"VALUES ({sql_val(ticker)}, {sql_val(sector)}, '{sg}', {has_loans}, {has_insurance}, {has_inventory}, {has_receivables}, {is_financial}, {is_holding}, {is_reit});"
    )
    sector_counts[sg] = sector_counts.get(sg, 0) + 1

with open(f"{OUT}/seed_isyatirim_ratios.sql", "w", encoding="utf-8") as f:
    f.write(f"-- Is Yatirim Reference Ratios (generated {NOW})\n")
    f.write(f"-- Source: is-yatirim-temel/*.xlsx\n\n")
    f.write("DELETE FROM isyatirim_ratios;\n\n")
    for line in ratios_lines:
        f.write(line + "\n")

with open(f"{OUT}/seed_company_metrics.sql", "w", encoding="utf-8") as f:
    f.write(f"-- Company Metrics Update from Is Yatirim Excel (generated {NOW})\n\n")
    f.write("DELETE FROM company_metrics;\n\n")
    for line in metrics_lines:
        f.write(line + "\n")

with open(f"{OUT}/seed_company_profiles.sql", "w", encoding="utf-8") as f:
    f.write(f"-- Company Sector Profiles (generated {NOW})\n\n")
    f.write("DELETE FROM company_sector_profiles;\n\n")
    for line in profit_lines:
        f.write(line + "\n")

print(f"Generated:")
print(f"  seed_isyatirim_ratios.sql: {len(ratios_lines)} rows")
print(f"  seed_company_metrics.sql:  {len(metrics_lines)} rows")
print(f"  seed_company_profiles.sql: {len(profit_lines)} rows")

print(f"\nSector Group Distribution:")
for k, v in sorted(sector_counts.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
