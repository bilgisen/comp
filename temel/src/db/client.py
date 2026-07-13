from typing import Optional, Any, List
from dataclasses import dataclass


@dataclass
class QueryResult:
    results: List[dict]
    success: bool
    error: Optional[str] = None

    @property
    def first(self) -> Optional[dict]:
        return self.results[0] if self.results else None


class D1Client:
    def __init__(self, db):
        self.db = db

    def _exec(self, sql: str, params: Optional[list] = None):
        stmt = self.db.prepare(sql)
        if params:
            stmt = stmt.bind(*params)
        return stmt

    async def query(self, sql: str, params: Optional[list] = None) -> QueryResult:
        try:
            stmt = self._exec(sql, params)
            d1_result = await stmt.all()
            rows = [dict(row) for row in d1_result.results] if d1_result.results else []
            return QueryResult(results=rows, success=d1_result.success)
        except Exception as e:
            return QueryResult(results=[], success=False, error=str(e))

    async def execute(self, sql: str, params: Optional[list] = None) -> QueryResult:
        return await self.query(sql, params)

    async def run(self, sql: str, params: Optional[list] = None) -> bool:
        try:
            stmt = self._exec(sql, params)
            await stmt.run()
            return True
        except Exception:
            return False

    async def insert(self, table: str, data: dict) -> bool:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return await self.run(sql, list(data.values()))

    async def insert_or_replace(self, table: str, data: dict) -> bool:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        return await self.run(sql, list(data.values()))
