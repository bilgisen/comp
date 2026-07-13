"""Fetch missing 36 tickers from Is Yatirim MaliTabloShortTable and generate SQL inserts for D1"""
import httpx
import json
import asyncio

MISSING = ["A1CAP", "AKGRT", "BRKVY", "CRDFA", "DOCO", "DSTKF", "EKDMR", "EKIM",
           "ENPRA", "GARFA", "GEDIK", "GLBMD", "GLCVY", "GOLDA", "INFO", "ISFIN",
           "ISKUR", "ISMEN", "KTLEV", "LIDFA", "MARMR", "ORZAX", "OSMEN", "OYYAT",
           "QNBFK", "RAYSG", "SEKFK", "SKYMD", "SMRVA", "SOHOE", "TERA", "UFUK",
           "ULUFA", "UNLU", "VAKFA", "VAKFN"]

BASE = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx"
PERIODS = [(2025, 6), (2025, 9), (2025, 12), (2026, 3)]

async def fetch_one(client, ticker):
    params = {"companyCode": ticker, "exchange": "TRY"}
    for i, (y, p) in enumerate(PERIODS, 1):
        params[f"year{i}"] = y
        params[f"period{i}"] = p
    try:
        r = await client.get(f"{BASE}/MaliTablo", params=params, timeout=30)
        data = r.json()
        if data.get("ok") and data.get("value"):
            items = data["value"]
            rows = []
            pk_map = {1: "2025Q2", 2: "2025Q3", 3: "2025Q4", 4: "2026Q1"}
            for item in items:
                code = item.get("kod", "")
                desc_tr = item.get("aciklama1", "")
                desc_en = item.get("itemDescEng", "")
                for i in range(1, 5):
                    val_key = f"valueTutar{i}" if f"valueTutar{i}" in item else f"value{i}"
                    raw = item.get(val_key)
                    if raw is not None:
                        try:
                            clean = str(raw).strip().replace(".", "").replace(",", ".")
                            val = float(clean)
                            y, p = PERIODS[i-1]
                            rows.append(f"('{ticker}','{pk_map[i]}',{y},{p},'XI_29','{code}','{desc_tr}','{desc_en}',{val},'TRY','2026-07-11T12:00:00')")
                        except (ValueError, AttributeError):
                            pass
            if rows:
                sql = "INSERT OR IGNORE INTO financial_statements_raw (ticker,period_key,year,period,financial_group,item_code,item_desc_tr,item_desc_en,value_try,currency,fetched_at) VALUES\n"
                sql += ",\n".join(rows) + ";"
                return [ticker, len(rows), sql]
            return [ticker, 0, None]
    except Exception as e:
        return [ticker, -1, str(e)[:100]]

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_one(client, t) for t in MISSING]
        results = await asyncio.gather(*tasks)
    
    all_sql = []
    success = 0
    for item in results:
        if item is None:
            continue
        ticker, count, data = item
        if count > 0:
            print(f"  {ticker}: {count} rows")
            all_sql.append(data)
            success += 1
        elif count == 0:
            print(f"  {ticker}: 0 rows (no data)")
        else:
            print(f"  {ticker}: ERROR - {data}")
    
    if all_sql:
        with open("C:\\Users\\ASUS\\hp\\comp\\seed_output\\seed_missing_36.sql", "w", encoding="utf-8") as f:
            f.write("\n\n".join(all_sql))
        print(f"\n** {success}/{len(MISSING)} tickers fetched. SQL written to seed_output/seed_missing_36.sql")
    else:
        print("\n** No data fetched!")

if __name__ == "__main__":
    asyncio.run(main())
