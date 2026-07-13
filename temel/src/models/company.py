from typing import Optional, List
from db.client import D1Client


class CompanyModel:
    def __init__(self, db: D1Client):
        self.db = db

    async def get_by_ticker(self, ticker: str) -> Optional[dict]:
        result = await self.db.query(
            "SELECT * FROM companies WHERE ticker = ? AND is_active = 1",
            [ticker.upper()]
        )
        return result.first

    async def get_all(self, page: int = 1, limit: int = 50, sector: Optional[str] = None) -> dict:
        offset = (page - 1) * limit
        where = "WHERE is_active = 1"
        params = []
        if sector:
            where += " AND sector_main = ?"
            params.append(sector)
        count_result = await self.db.query(f"SELECT COUNT(*) as total FROM companies {where}", params)
        total = count_result.first["total"] if count_result.first else 0
        result = await self.db.query(
            f"SELECT * FROM companies {where} ORDER BY market_cap DESC LIMIT ? OFFSET ?",
            params + [limit, offset]
        )
        return {
            "companies": result.results,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": -(-total // limit) if total > 0 else 0
        }

    async def get_sectors(self) -> List[dict]:
        result = await self.db.query(
            "SELECT sector_main, COUNT(*) as count FROM companies WHERE is_active = 1 GROUP BY sector_main ORDER BY count DESC"
        )
        return result.results

    async def search(self, query: str, limit: int = 20) -> List[dict]:
        result = await self.db.query(
            "SELECT * FROM companies WHERE (ticker LIKE ? OR name LIKE ?) AND is_active = 1 LIMIT ?",
            [f"%{query.upper()}%", f"%{query}%", limit]
        )
        return result.results

    async def upsert_company(self, data: dict) -> bool:
        return await self.db.insert_or_replace("companies", data)
