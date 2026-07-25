from typing import Optional
from db.client import D1Client

SECTOR_GROUP_NAMES = {
    "Bankacilik_Finans": "Bankacılık & Finans",
    "Sigortacilik": "Sigortacılık",
    "GYO": "GYO",
    "Enerji_Altyapi": "Enerji & Altyapı",
    "Sanayi_Metal_Kimya": "Sanayi & Metal & Kimya",
    "Insaat_Yapi": "İnşaat & Yapı Malzemeleri",
    "Otomotiv_Savunma_Makine": "Otomotiv & Savunma & Makine",
    "Saglik_Ilac": "Sağlık & İlaç",
    "Teknoloji_Iletisim": "Teknoloji & İletişim",
    "Gida_Icecek_Tarim": "Gıda & İçecek & Tarım",
    "Tuketim_Perakende_Tekstil": "Tüketim & Perakende & Tekstil",
    "Ulastirma_Lojistik": "Ulaştırma & Lojistik",
    "Turizm_Medya_Eglence": "Turizm & Medya & Eğlence",
    "Holdingler": "Holdingler",
}

RATIO_CATEGORIES = {
    "pe": "valuation", "pb": "valuation", "ev_ebitda": "valuation", "ev_sales": "valuation",
    "roe": "profitability", "roa": "profitability", "net_margin": "profitability",
    "gross_margin": "profitability", "profit_growth": "profitability",
    "current_ratio": "liquidity", "cash_ratio": "liquidity",
    "debt_equity": "leverage", "interest_coverage": "leverage",
}

RATIO_NAMES_SHORT = {
    "pe": "F/K", "pb": "PD/DD", "ev_ebitda": "FD/FAVÖK", "ev_sales": "FD/Satışlar",
    "roe": "ROE", "roa": "ROA", "net_margin": "Net Kâr Marjı",
    "gross_margin": "Brüt Kâr Marjı", "profit_growth": "Kâr Büyümesi",
    "current_ratio": "Cari Oran", "cash_ratio": "Nakit Oranı",
    "debt_equity": "Borç/Özkaynak", "interest_coverage": "Faiz Karşılama",
}


class SectorContextBuilder:
    def __init__(self, db: D1Client):
        self.db = db

    async def build(self, sector_name: str, period_key: str = "TTM") -> dict:
        raw_sector = await self._resolve_sector(sector_name)
        if not raw_sector:
            return {"error": f"Sector '{sector_name}' not found"}, 404

        company_count = await self._company_count(raw_sector)
        if company_count == 0:
            return {"error": f"No active companies in sector '{raw_sector}'"}, 404

        companies_with_data = await self._companies_with_data_count(raw_sector, period_key)
        consolidated = await self._get_consolidated(raw_sector)
        group_name = SECTOR_GROUP_NAMES.get(consolidated) if consolidated else None

        sector_benchmarks = await self._get_benchmarks(raw_sector, "sector", period_key)
        group_benchmarks = await self._get_benchmarks(consolidated, "group", period_key) if consolidated else {}
        market_benchmarks = await self._get_benchmarks("bist_all", "market", period_key)

        benchmarks = sector_benchmarks or group_benchmarks or market_benchmarks or {}
        benchmark_source = "sector" if sector_benchmarks else ("group" if group_benchmarks else ("market" if market_benchmarks else None))
        benchmark_name = raw_sector if benchmark_source == "sector" else (consolidated if benchmark_source == "group" else "BIST Tüm")

        leaders = await self._get_leaders(raw_sector, period_key, limit=20)
        sector_health = self._compute_sector_health(leaders)

        return {
            "sector": raw_sector,
            "consolidated_group": consolidated,
            "consolidated_name": group_name,
            "company_count": company_count,
            "companies_with_data": companies_with_data,
            "data_coverage_pct": round(companies_with_data / company_count * 100, 1) if company_count > 0 else 0,
            "benchmark_source": benchmark_source,
            "benchmark_name": benchmark_name,
            "n_peers": self._get_benchmark_n(benchmarks),
            "reliability": self._get_benchmark_reliability(benchmarks),
            "benchmarks": benchmarks,
            "sector_health": sector_health,
            "leaders": leaders[:10],
            "all_peers": [l["ticker"] for l in leaders],
        }

    async def _resolve_sector(self, name: str) -> Optional[str]:
        name_clean = name.replace("_", " ").strip()
        name_lower = name_clean.lower()
        candidates = []

        for table, col in [("companies", "sector_main"), ("sector_consolidation", "sector_raw"),
                           ("sector_consolidation", "sector_consolidated")]:
            r = await self.db.query(
                f"SELECT DISTINCT {col} as name FROM {table} WHERE LOWER({col}) = LOWER(?) LIMIT 1",
                [name_clean]
            )
            if r.first:
                candidates.append(r.first["name"])

        for col in ["sector_main", "sector_raw"]:
            r = await self.db.query(
                f"SELECT DISTINCT {col} as name FROM companies WHERE LOWER({col}) LIKE ? LIMIT 1",
                [f"%{name_lower}%"]
            )
            if r.first:
                candidates.append(r.first["name"])

        for group_key, group_name in SECTOR_GROUP_NAMES.items():
            normalized_key = group_key.lower().replace("_", " ")
            normalized_name = group_name.lower()
            if name_lower in (normalized_key, normalized_name):
                r = await self.db.query(
                    "SELECT DISTINCT sector_raw as name FROM sector_consolidation WHERE sector_consolidated = ? LIMIT 1",
                    [group_key]
                )
                if r.first:
                    return r.first["name"]

        if candidates:
            return candidates[0]

        all_sectors = await self.db.query(
            "SELECT DISTINCT sector_main FROM companies WHERE is_active = 1 ORDER BY sector_main"
        )
        for row in all_sectors.results:
            if name_lower in row["sector_main"].lower():
                return row["sector_main"]

        return None

    async def _company_count(self, sector: str) -> int:
        r = await self.db.query(
            "SELECT COUNT(*) as cnt FROM companies WHERE (sector_main = ? OR sector_raw = ?) AND is_active = 1",
            [sector, sector]
        )
        return r.first["cnt"] if r.first else 0

    async def _companies_with_data_count(self, sector: str, period_key: str) -> int:
        r = await self.db.query(
            "SELECT COUNT(DISTINCT cr.ticker) as cnt FROM company_ratios cr JOIN companies c ON cr.ticker = c.ticker WHERE c.sector_main = ? AND cr.period_key = ? AND cr.ratio_value IS NOT NULL",
            [sector, period_key]
        )
        return r.first["cnt"] if r.first else 0

    async def _get_consolidated(self, sector: str) -> Optional[str]:
        r = await self.db.query(
            "SELECT sector_consolidated FROM sector_consolidation WHERE sector_raw = ? LIMIT 1",
            [sector]
        )
        if r.first:
            return r.first["sector_consolidated"]
        r2 = await self.db.query(
            "SELECT DISTINCT sector_consolidated FROM sector_consolidation WHERE sector_consolidated = ? LIMIT 1",
            [sector]
        )
        return r2.first["sector_consolidated"] if r2.first else None

    async def _get_benchmarks(self, sector_name: str, btype: str, period_key: str) -> dict:
        if not sector_name:
            return {}
        r = await self.db.query(
            "SELECT * FROM sector_benchmarks WHERE sector_name = ? AND benchmark_type = ? AND period_key = ? ORDER BY ratio_code",
            [sector_name, btype, period_key]
        )
        if not r.results:
            return {}
        result = {}
        for row in r.results:
            rc = row["ratio_code"]
            result[rc] = {
                "median_ew": row.get("median_ew"),
                "median_mc": row.get("median_mc"),
                "p25": row.get("p25"),
                "p75": row.get("p75"),
                "n_peers": row.get("n_peers"),
                "reliability": row.get("reliability"),
                "name": RATIO_NAMES_SHORT.get(rc, rc),
                "category": RATIO_CATEGORIES.get(rc, "other"),
            }
        return result

    def _get_benchmark_n(self, benchmarks: dict) -> Optional[int]:
        for rc, data in benchmarks.items():
            if data.get("n_peers"):
                return data["n_peers"]
        return None

    def _get_benchmark_reliability(self, benchmarks: dict) -> Optional[str]:
        rels = [data["reliability"] for data in benchmarks.values() if data.get("reliability")]
        if "HIGH" in rels:
            return "HIGH"
        if "MEDIUM" in rels:
            return "MEDIUM"
        if "LOW" in rels:
            return "LOW"
        if "INSUFFICIENT" in rels:
            return "INSUFFICIENT"
        return None

    async def _get_leaders(self, sector: str, period_key: str, limit: int = 20) -> list:
        r = await self.db.query(
            """SELECT cs.ticker, c.name, cs.composite_score, cs.absolute_score, cs.absolute_label,
                      cs.pillar_finansal_saglik, cs.pillar_karlilik_buyume, cs.pillar_degerleme,
                      cs.reliability, c.market_cap
               FROM company_scores cs
               JOIN companies c ON cs.ticker = c.ticker
               WHERE c.sector_main = ? AND cs.period_key = ? AND cs.composite_score IS NOT NULL
               ORDER BY cs.composite_score DESC LIMIT ?""",
            [sector, period_key, limit]
        )
        leaders = []
        for i, row in enumerate(r.results):
            leaders.append({
                "rank": i + 1,
                "ticker": row["ticker"],
                "name": row["name"],
                "composite_score": row["composite_score"],
                "absolute_score": row["absolute_score"],
                "absolute_label": row["absolute_label"],
                "pillars": {
                    "finansal_saglik": row.get("pillar_finansal_saglik"),
                    "karlilik_buyume": row.get("pillar_karlilik_buyume"),
                    "degerleme": row.get("pillar_degerleme"),
                },
                "reliability": row.get("reliability"),
                "market_cap": row.get("market_cap"),
            })
        return leaders

    def _compute_sector_health(self, leaders: list) -> dict:
        scores = [l["composite_score"] for l in leaders if l["composite_score"] is not None]
        if not scores:
            return {"composite_score": None, "status": "unknown", "n_scored": 0}

        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        median = sorted_scores[n // 2] if n % 2 else (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2

        if median >= 65:
            status = "guclu"
        elif median >= 50:
            status = "saglikli"
        elif median >= 35:
            status = "orta"
        else:
            status = "zayif"

        abs_labels = [l["absolute_label"] for l in leaders if l.get("absolute_label")]
        strong_count = sum(1 for lbl in abs_labels if lbl in ("GUCLU", "SAGLIKLI"))
        weak_count = sum(1 for lbl in abs_labels if lbl in ("ZAYIF", "KRITIK"))

        return {
            "composite_score": round(median, 1),
            "status": status,
            "n_scored": n,
            "strong_count": strong_count,
            "weak_count": weak_count,
            "average_score": round(sum(scores) / len(scores), 1) if scores else None,
        }
