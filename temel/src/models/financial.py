from typing import Optional, List
from db.client import D1Client


class FinancialModel:
    def __init__(self, db: D1Client):
        self.db = db

    async def get_statements(self, ticker: str, period_key: Optional[str] = None, limit: int = 100) -> List[dict]:
        if period_key:
            result = await self.db.query(
                """SELECT * FROM financial_statements_raw 
                   WHERE ticker = ? AND period_key = ? 
                   ORDER BY year DESC, period DESC LIMIT ?""",
                [ticker.upper(), period_key, limit]
            )
        else:
            result = await self.db.query(
                """SELECT * FROM financial_statements_raw 
                   WHERE ticker = ? 
                   ORDER BY year DESC, period DESC LIMIT ?""",
                [ticker.upper(), limit]
            )
        return result.results

    async def get_distinct_periods(self, ticker: str) -> List[str]:
        result = await self.db.query(
            "SELECT DISTINCT period_key FROM financial_statements_raw WHERE ticker = ? ORDER BY period_key DESC",
            [ticker.upper()]
        )
        return [r["period_key"] for r in result.results]

    async def get_ratios(self, ticker: str, period_key: Optional[str] = None, ratio_codes: Optional[List[str]] = None) -> List[dict]:
        where = "WHERE ticker = ?"
        params = [ticker.upper()]
        if period_key:
            where += " AND period_key = ?"
            params.append(period_key)
        if ratio_codes:
            placeholders = ", ".join(["?" for _ in ratio_codes])
            where += f" AND ratio_code IN ({placeholders})"
            params.extend(ratio_codes)
        result = await self.db.query(
            f"SELECT * FROM company_ratios {where} ORDER BY ratio_code",
            params
        )
        return result.results

    async def get_latest_period(self, ticker: str) -> Optional[str]:
        result = await self.db.query(
            "SELECT period_key FROM company_ratios WHERE ticker = ? ORDER BY (period_key = 'TTM') DESC, computed_at DESC LIMIT 1",
            [ticker.upper()]
        )
        return result.first["period_key"] if result.first else None

    async def get_global_latest_period(self) -> Optional[str]:
        result = await self.db.query(
            "SELECT period_key FROM company_ratios ORDER BY computed_at DESC LIMIT 1"
        )
        return result.first["period_key"] if result.first else None

    async def save_ratios(self, ratios: list) -> int:
        saved = 0
        for r in ratios:
            ok = await self.db.insert_or_replace("company_ratios", {
                "ticker": r["ticker"],
                "period_key": r["period_key"],
                "ratio_code": r["ratio_code"],
                "ratio_value": r.get("ratio_value"),
                "is_ttm": 1 if r.get("is_ttm") else 0,
                "calculation_method": r.get("calculation_method"),
                "data_quality_score": r.get("data_quality_score"),
                "computed_at": r.get("computed_at")
            })
            if ok:
                saved += 1
        return saved

    async def save_statements(self, statements: list) -> int:
        saved = 0
        for s in statements:
            ok = await self.db.insert_or_replace("financial_statements_raw", {
                "ticker": s["ticker"],
                "period_key": s["period_key"],
                "year": s["year"],
                "period": s["period"],
                "financial_group": s["financial_group"],
                "item_code": s["item_code"],
                "item_desc_tr": s.get("item_desc_tr"),
                "value_try": s.get("value_try"),
                "currency": s.get("currency", "TRY"),
                "fetched_at": s.get("fetched_at")
            })
            if ok:
                saved += 1
        return saved

    async def get_item_code_mappings(self, financial_group: str) -> List[dict]:
        result = await self.db.query(
            "SELECT * FROM item_code_mappings WHERE financial_group = ? ORDER BY priority",
            [financial_group]
        )
        return result.results

    async def get_financial_summary(self, ticker: str, period_key: Optional[str] = None) -> List[dict]:
        if period_key:
            result = await self.db.query(
                "SELECT * FROM company_financial_summary WHERE ticker = ? AND period_key = ? ORDER BY period_key DESC",
                [ticker.upper(), period_key]
            )
        else:
            result = await self.db.query(
                "SELECT * FROM company_financial_summary WHERE ticker = ? ORDER BY period_key DESC LIMIT 4",
                [ticker.upper()]
            )
        return result.results
