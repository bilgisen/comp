from typing import Optional
from db.client import D1Client


class MetricsModel:
    def __init__(self, db: D1Client):
        self.db = db

    async def get_by_ticker(self, ticker: str) -> Optional[dict]:
        result = await self.db.query(
            "SELECT * FROM company_metrics WHERE ticker = ?",
            [ticker.upper()]
        )
        return result.first

    async def upsert(self, ticker: str, data: dict) -> bool:
        data["ticker"] = ticker.upper()
        return await self.db.insert_or_replace("company_metrics", data)

    async def get_top_by_market_cap(self, sector: Optional[str] = None, limit: int = 10) -> list:
        where = "WHERE cm.market_cap IS NOT NULL"
        params = []
        if sector:
            where += " AND c.sector_main = ?"
            params.append(sector)
        result = await self.db.query(
            f"""SELECT c.ticker, c.name, c.sector_main, cm.last_price, cm.market_cap, cm.pe_ratio, cm.pb_ratio
                FROM company_metrics cm
                JOIN companies c ON cm.ticker = c.ticker
                {where}
                ORDER BY cm.market_cap DESC LIMIT ?""",
            params + [limit]
        )
        return result.results
