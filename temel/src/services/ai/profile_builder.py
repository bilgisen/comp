from typing import Optional
from db.client import D1Client


class ProfileBuilder:
    def __init__(self, db: D1Client):
        self.db = db

    async def build(self, ticker: str) -> Optional[dict]:
        r = await self.db.query(
            "SELECT ticker, name, sector_main, industry, financial_group, market_cap, shares_outstanding, free_float_pct, about, website, city FROM companies WHERE ticker = ? AND is_active = 1",
            [ticker.upper()]
        )
        if not r.first:
            return None
        c = r.first

        m = await self.db.query(
            "SELECT last_price, market_cap, volume_1d, volume_avg_30d FROM company_metrics WHERE ticker = ?",
            [ticker.upper()]
        )

        mcap = c.get("market_cap") or (m.first["market_cap"] if m.first else None)
        last_price = m.first["last_price"] if m.first else None

        return {
            "ticker": c["ticker"],
            "name": c["name"],
            "sector": c.get("sector_main"),
            "industry": c.get("industry"),
            "financial_group": c.get("financial_group"),
            "market_cap": mcap,
            "market_cap_formatted": self._fmt_mcap(mcap) if mcap else None,
            "last_price": last_price,
            "shares_outstanding": c.get("shares_outstanding"),
            "free_float_pct": c.get("free_float_pct"),
            "city": c.get("city"),
            "website": c.get("website"),
            "about": c.get("about"),
        }

    def _fmt_mcap(self, mcap):
        if mcap >= 1_000_000_000:
            return f"{mcap / 1_000_000_000:.1f} Milyar TL"
        if mcap >= 1_000_000:
            return f"{mcap / 1_000_000:.1f} Milyon TL"
        return f"{mcap / 1_000:.1f} Bin TL"
