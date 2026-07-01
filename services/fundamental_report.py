"""
CEO-Level Fundamental Analysis Report Service
Generates comprehensive, actionable fundamental analysis reports
without tiered access restrictions.

All members get full access to CEO-level reports.
"""

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

from sqlalchemy.orm import Session
from sqlalchemy import text

logger = logging.getLogger(__name__)


@dataclass
class FundamentalReport:
    """CEO-Level Fundamental Analysis Report"""
    ticker: str
    company_name: str
    sector: str
    period_key: str

    # Executive Summary
    executive_summary: str

    # Financial Health
    financial_health: Dict[str, Any]

    # Profitability Analysis
    profitability: Dict[str, Any]

    # Sector Comparison
    sector_comparison: Dict[str, Any]

    # SWOT Analysis
    swot: Dict[str, Any]

    # Scenario Analysis
    scenarios: Dict[str, Any]

    # Watchlist
    watchlist: List[Dict[str, str]]

    # Metadata
    computed_at: datetime = field(default_factory=datetime.utcnow)
    disclaimer: str = "Bu analiz otomatik veri analizine dayanmaktadır ve yatırım tavsiyesi değildir."


class FundamentalReportService:
    """
    Generates CEO-level fundamental analysis reports.

    Uses actual ratio data, score cards, sector benchmarks, and SWOT analysis
    to produce actionable investment insights.
    """

    def __init__(self, db: Session):
        self.db = db

    def generate(self, ticker: str, period_key: Optional[str] = None) -> Optional[FundamentalReport]:
        """Generate a full CEO-level fundamental report for the given ticker."""

        ticker = ticker.upper()

        # Get company info
        company = self.db.execute(text("""
            SELECT ticker, name, sector_main
            FROM companies
            WHERE ticker = :ticker AND is_active = TRUE
        """), {"ticker": ticker}).fetchone()

        if not company:
            return None

        # Get latest period if not specified
        if not period_key:
            period_key = self.db.execute(text("""
                SELECT MAX(period_key) FROM company_scores WHERE ticker = :ticker
            """), {"ticker": ticker}).scalar()

        if not period_key:
            return None

        # Gather all data
        score_card = self._get_score_card(ticker, period_key)
        ratio_cards = self._get_ratio_comparisons(ticker, period_key)
        sector_position = self._get_sector_position(ticker, period_key)
        swot_card = self._get_swot(ticker, period_key)
        trend_data = self._get_trend_summary(ticker, period_key)

        # Build report sections
        exec_summary = self._build_executive_summary(
            company, score_card, ratio_cards, sector_position
        )
        financial_health = self._build_financial_health(ratio_cards)
        profitability = self._build_profitability(ratio_cards, score_card)
        sector_comparison = self._build_sector_comparison(sector_position, ratio_cards)
        swot_section = self._build_swot_section(swot_card)
        scenarios = self._build_scenarios(score_card, ratio_cards, swot_card)
        watchlist = self._build_watchlist(ratio_cards, score_card, sector_position)

        return FundamentalReport(
            ticker=ticker,
            company_name=company.name,
            sector=company.sector_main,
            period_key=period_key,
            executive_summary=exec_summary,
            financial_health=financial_health,
            profitability=profitability,
            sector_comparison=sector_comparison,
            swot=swot_section,
            scenarios=scenarios,
            watchlist=watchlist,
        )

    # ───────────────────────────────────────────────────────────────────
    # DATA FETCHING
    # ───────────────────────────────────────────────────────────────────

    def _get_score_card(self, ticker: str, period_key: str) -> Optional[Dict]:
        """Fetch score card data."""
        row = self.db.execute(text("""
            SELECT
                cs.score_sektor, cs.score_genel,
                cs.score_karlilik, cs.score_finansal, cs.score_verimlilik, cs.score_degerleme,
                cs.reliability_sektor, cs.n_peers_sektor,
                c.sector_main
            FROM company_scores cs
            JOIN companies c ON cs.ticker = c.ticker
            WHERE cs.ticker = :ticker AND cs.period_key = :period_key
        """), {"ticker": ticker, "period_key": period_key}).fetchone()

        if not row:
            return None

        # Calculate rank
        rank_row = self.db.execute(text("""
            SELECT COUNT(*) + 1 as rank
            FROM company_scores cs
            JOIN companies c ON cs.ticker = c.ticker
            WHERE c.sector_main = :sector
              AND cs.period_key = :period_key
              AND cs.score_sektor > :score
        """), {
            "sector": row.sector_main,
            "period_key": period_key,
            "score": row.score_sektor or 0
        }).fetchone()

        rank = rank_row.rank if rank_row else 1
        percentile = int(100 - (rank / max(row.n_peers_sektor or 1, 1)) * 100)

        return {
            "score_sektor": float(row.score_sektor) if row.score_sektor else None,
            "score_genel": float(row.score_genel) if row.score_genel else None,
            "score_karlilik": float(row.score_karlilik) if row.score_karlilik else None,
            "score_finansal": float(row.score_finansal) if row.score_finansal else None,
            "score_verimlilik": float(row.score_verimlilik) if row.score_verimlilik else None,
            "score_degerleme": float(row.score_degerleme) if row.score_degerleme else None,
            "reliability": row.reliability_sektor,
            "percentile_sector": percentile,
            "rank_sector": rank,
            "total_peers": row.n_peers_sektor,
        }

    def _get_ratio_comparisons(self, ticker: str, period_key: str) -> List[Dict]:
        """Fetch all ratio comparisons with sector benchmarks."""
        rows = self.db.execute(text("""
            SELECT
                cr.ratio_code, cr.ratio_value,
                sb.median_ew as sector_median,
                sb.p25, sb.p75
            FROM company_ratios cr
            LEFT JOIN companies c ON cr.ticker = c.ticker
            LEFT JOIN sector_benchmarks sb
                ON sb.ratio_code = cr.ratio_code
                AND sb.sector_main = c.sector_main
                AND sb.period_key = cr.period_key
            WHERE cr.ticker = :ticker
              AND cr.period_key = :period_key
              AND cr.ratio_value IS NOT NULL
        """), {"ticker": ticker, "period_key": period_key}).fetchall()

        RATIO_NAMES = {
            "roe": "Özkaynak Kârlılığı (ROE)",
            "roa": "Aktif Kârlılığı (ROA)",
            "gross_margin": "Brüt Kâr Marjı",
            "net_margin": "Net Kâr Marjı",
            "operating_margin": "Faaliyet Kâr Marjı",
            "ebitda_margin": "FAVÖK Marjı",
            "current_ratio": "Cari Oran",
            "acid_test_ratio": "Asit Test Oranı",
            "debt_ratio": "Borçlanma Oranı",
            "debt_to_equity": "Borç/Özkaynak",
            "net_debt_to_equity": "Net Borç/Özkaynak",
            "asset_turnover": "Aktif Devir Hızı",
            "cost_income_ratio": "Maliyet/Gelir",
            "loan_to_deposit": "Kredi/Mevduat",
            "npl_ratio": "Takipteki Kredi",
            "capital_adequacy": "Sermaye Yeterlilik",
            "net_interest_margin": "Net Faiz Marjı",
        }

        cards = []
        for row in rows:
            val = float(row.ratio_value) if row.ratio_value else None
            med = float(row.sector_median) if row.sector_median else None
            p25 = float(row.p25) if row.p25 else None
            p75 = float(row.p75) if row.p75 else None

            percentile = 50
            if val is not None and med is not None:
                below = sum(1 for v in [med] if v < val)
                percentile = int((below / 1) * 100) if med else 50
                if val > (p75 or med):
                    percentile = 75
                elif val < (p25 or med):
                    percentile = 25

            diff_pct = 0
            if med and med != 0 and val is not None:
                diff_pct = ((val - med) / abs(med)) * 100

            interpretation = self._interpret_ratio(row.ratio_code, val, med, diff_pct)

            cards.append({
                "ratio_code": row.ratio_code,
                "ratio_name": RATIO_NAMES.get(row.ratio_code, row.ratio_code),
                "company_value": val,
                "sector_median": med,
                "sector_p25": p25,
                "sector_p75": p75,
                "percentile": percentile,
                "diff_pct": round(diff_pct, 1),
                "interpretation": interpretation,
            })

        return cards

    def _get_sector_position(self, ticker: str, period_key: str) -> Optional[Dict]:
        """Get sector ranking and position."""
        row = self.db.execute(text("""
            SELECT
                c.sector_main,
                cs.score_sektor,
                cs.n_peers_sektor,
                RANK() OVER (
                    PARTITION BY c.sector_main
                    ORDER BY cs.score_sektor DESC NULLS LAST
                ) as sector_rank
            FROM company_scores cs
            JOIN companies c ON cs.ticker = c.ticker
            WHERE cs.ticker = :ticker AND cs.period_key = :period_key
        """), {"ticker": ticker, "period_key": period_key}).fetchone()

        if not row:
            return None

        # Get above/below median ratios
        ratio_perf = self.db.execute(text("""
            SELECT
                cr.ratio_code,
                CASE WHEN cr.ratio_value > sb.median_ew THEN 'above' ELSE 'below' END as position
            FROM company_ratios cr
            JOIN sector_benchmarks sb
                ON sb.ratio_code = cr.ratio_code
                AND sb.sector_main = :sector
                AND sb.period_key = cr.period_key
            WHERE cr.ticker = :ticker AND cr.period_key = :period_key
        """), {"ticker": ticker, "sector": row.sector_main, "period_key": period_key}).fetchall()

        above = [r.ratio_code for r in ratio_perf if r.position == 'above']
        below = [r.ratio_code for r in ratio_perf if r.position == 'below']

        return {
            "sector_name": row.sector_main,
            "total_companies": row.n_peers_sektor or 1,
            "rank": int(row.sector_rank) if row.sector_rank else 1,
            "percentile": float(row.score_sektor) if row.score_sektor else 50.0,
            "above_median_ratios": above,
            "below_median_ratios": below,
        }

    def _get_swot(self, ticker: str, period_key: str) -> Dict[str, Any]:
        """Generate SWOT analysis from ratio data."""
        ratios = self.db.execute(text("""
            SELECT
                cr.ratio_code, cr.ratio_value,
                sb.median_ew as sector_median,
                sb.p25, sb.p75,
                CASE
                    WHEN cr.ratio_value IS NULL THEN NULL
                    WHEN sb.median_ew IS NULL THEN NULL
                    WHEN cr.ratio_value > sb.p75 THEN 'above_high'
                    WHEN cr.ratio_value > sb.median_ew THEN 'above_median'
                    WHEN cr.ratio_value > sb.p25 THEN 'below_median'
                    ELSE 'below_low'
                END as position
            FROM company_ratios cr
            LEFT JOIN companies c ON cr.ticker = c.ticker
            LEFT JOIN sector_benchmarks sb
                ON sb.ratio_code = cr.ratio_code
                AND sb.sector_main = c.sector_main
                AND sb.period_key = cr.period_key
            WHERE cr.ticker = :ticker AND cr.period_key = :period_key
              AND cr.ratio_value IS NOT NULL
        """), {"ticker": ticker, "period_key": period_key}).fetchall()

        scores = self.db.execute(text("""
            SELECT score_sektor, score_karlilik, score_finansal, score_verimlilik, score_degerleme
            FROM company_scores
            WHERE ticker = :ticker AND period_key = :period_key
        """), {"ticker": ticker, "period_key": period_key}).fetchone()

        RATIO_LABELS = {
            "roe": "Özkaynak kârlılığı", "roa": "Aktif kârlılığı",
            "gross_margin": "Brüt kâr marjı", "net_margin": "Net kâr marjı",
            "operating_margin": "Operasyonel marj", "ebitda_margin": "FAVÖK marjı",
            "current_ratio": "Cari oran", "acid_test_ratio": "Asit test oranı",
            "debt_ratio": "Borçlanma oranı", "debt_to_equity": "Borç/Özsermaye",
            "net_debt_to_equity": "Net borç/Özsermaye", "asset_turnover": "Aktif devir hızı",
            "npl_ratio": "Takipteki kredi oranı", "capital_adequacy": "Sermaye yeterlilik",
            "net_interest_margin": "Net faiz marjı",
        }

        STRENGTH_RATIOS = {
            "roe", "roa", "gross_margin", "net_margin", "operating_margin", "ebitda_margin",
            "current_ratio", "acid_test_ratio", "asset_turnover", "net_interest_margin", "capital_adequacy"
        }
        WEAKNESS_RATIOS = {"debt_ratio", "debt_to_equity", "net_debt_to_equity", "npl_ratio"}

        strengths, weaknesses, opportunities, threats = [], [], [], []

        for row in ratios:
            label = RATIO_LABELS.get(row.ratio_code, row.ratio_code)
            pos = row.position
            val = float(row.ratio_value) if row.ratio_value else None
            med = float(row.sector_median) if row.sector_median else None

            if pos is None or val is None:
                continue

            diff_pct = ((val - med) / abs(med) * 100) if med and med != 0 else 0

            if pos == "above_high" and row.ratio_code in STRENGTH_RATIOS:
                impact = "high" if diff_pct > 20 else "medium"
                item = f"{label} sektör ortalamasının %{abs(diff_pct):.0f} üzerinde" if diff_pct > 20 else f"{label} sektör üst çeyreğinde"
                strengths.append({"item": item, "impact": impact, "source": row.ratio_code})

            elif pos == "below_low" and row.ratio_code in WEAKNESS_RATIOS:
                impact = "high" if abs(diff_pct) > 20 else "medium"
                item = f"{label} sektör ortalamasının belirgin şekilde altında" if abs(diff_pct) > 20 else f"{label} sektör alt çeyreğinde"
                weaknesses.append({"item": item, "impact": impact, "source": row.ratio_code})

            elif pos == "below_low" and row.ratio_code in STRENGTH_RATIOS:
                weaknesses.append({"item": f"{label} sektör ortalamasının altında", "impact": "medium", "source": row.ratio_code})

            elif pos == "above_high" and row.ratio_code in WEAKNESS_RATIOS:
                weaknesses.append({"item": f"{label} sektör ortalamasının üzerinde (risk)", "impact": "medium", "source": row.ratio_code})

        if scores:
            if scores.score_karlilik and float(scores.score_karlilik) > 70:
                strengths.append({"item": "Güçlü kârlılık performansı", "impact": "high", "source": "score_karlilik"})
            elif scores.score_karlilik and float(scores.score_karlilik) < 40:
                weaknesses.append({"item": "Kârlılık performansı düşük", "impact": "high", "source": "score_karlilik"})

        # Sector pattern
        above_count = sum(1 for r in ratios if r.position in ("above_high", "above_median"))
        below_count = sum(1 for r in ratios if r.position in ("below_low", "below_median"))
        total = len(ratios) if ratios else 1

        if above_count > total * 0.6:
            opportunities.append({"item": "Sektör ortalamasının üzerinde performans — büyüme potansiyeli güçlü", "impact": "high", "source": "sector_pattern"})
        elif below_count > total * 0.6:
            threats.append({"item": "Çoğunlukla sektörün altında performans", "impact": "high", "source": "sector_pattern"})

        # Liquidity
        cr_row = next((r for r in ratios if r.ratio_code == "current_ratio"), None)
        if cr_row and cr_row.position == "above_high":
            opportunities.append({"item": "Güçlü likidite — büyüme yatırımları için kaynak mevcut", "impact": "medium", "source": "current_ratio"})
        elif cr_row and cr_row.position == "below_low":
            threats.append({"item": "Düşük likidite — kısa vadeli borç ödeme riski", "impact": "high", "source": "current_ratio"})

        # Debt
        dr_row = next((r for r in ratios if r.ratio_code == "debt_ratio"), None)
        if dr_row and dr_row.position == "below_low":
            opportunities.append({"item": "Düşük borçlanma — finansal esneklik yüksek", "impact": "medium", "source": "debt_ratio"})
        elif dr_row and dr_row.position == "above_high":
            threats.append({"item": "Yüksek borçlanma — faiz artışı riski", "impact": "high", "source": "debt_ratio"})

        # Defaults
        if not strengths:
            strengths.append({"item": "Sektördeki konumunu koruyor", "impact": "low", "source": "general"})
        if not weaknesses:
            weaknesses.append({"item": "Belirgin zayıf yön tespit edilemedi", "impact": "low", "source": "general"})
        if not opportunities:
            opportunities.append({"item": "Sektör dinamiklerine göre konumunu değerlendirilmeli", "impact": "low", "source": "general"})
        if not threats:
            threats.append({"item": "Piyasa koşullarına dikkat edilmeli", "impact": "low", "source": "general"})

        return {
            "strengths": strengths[:5],
            "weaknesses": weaknesses[:5],
            "opportunities": opportunities[:5],
            "threats": threats[:5],
        }

    def _get_trend_summary(self, ticker: str, period_key: str) -> Optional[Dict]:
        """Get basic trend data from recent periods."""
        rows = self.db.execute(text("""
            SELECT period_key, score_sektor, score_karlilik
            FROM company_scores
            WHERE ticker = :ticker
            ORDER BY period_key DESC
            LIMIT 4
        """), {"ticker": ticker}).fetchall()

        if not rows or len(rows) < 2:
            return None

        latest = float(rows[0].score_sektor) if rows[0].score_sektor else None
        prev = float(rows[1].score_sektor) if rows[1].score_sektor else None

        if latest is not None and prev is not None:
            change = latest - prev
            if change > 5:
                direction = "improving"
            elif change < -5:
                direction = "declining"
            else:
                direction = "stable"
        else:
            direction = "unknown"
            change = 0

        return {
            "periods": [r.period_key for r in rows],
            "scores": [float(r.score_sektor) if r.score_sektor else None for r in rows],
            "direction": direction,
            "change": round(change, 1),
        }

    # ───────────────────────────────────────────────────────────────────
    # REPORT SECTION BUILDERS
    # ───────────────────────────────────────────────────────────────────

    def _interpret_ratio(self, ratio_code: str, val: Optional[float], med: Optional[float], diff_pct: float) -> str:
        """Generate CEO-level interpretation for a ratio."""
        if val is None:
            return f"{ratio_code} verisi mevcut değil."

        direction = "yüksek" if diff_pct > 0 else "düşük"
        magnitude = "belirgin şekilde" if abs(diff_pct) > 20 else "hafif"

        interpretations = {
            "roe": f"Özkaynak kârlılığı sektör ortalamasına göre %{abs(diff_pct):.1f} {magnitude} {direction}. {'Güçlü getiri potansiyeli gösteriyor.' if diff_pct > 10 else 'İyileştirme alanı mevcut.'}",
            "roa": f"Aktif kârlılığı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Varlık kullanım verimliliği güçlü.' if diff_pct > 10 else 'Varlık kullanımında optimizasyon potansiyeli var.'}",
            "gross_margin": f"Brüt kâr marjı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Fiyatlama gücü ve maliyet kontrolü sağlıklı.' if diff_pct > 10 else 'Fiyatlandırma veya maliyet yapısında baskı var.'}",
            "net_margin": f"Net kâr marjı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Sonuç kârlılığı güçlü.' if diff_pct > 10 else 'Gider yönetimi iyileştirilebilir.'}",
            "operating_margin": f"Faaliyet kâr marjı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Operasyonel verimlilik yüksek.' if diff_pct > 10 else 'Operasyonel giderlerde optimizasyon gerekebilir.'}",
            "ebitda_margin": f"FAVÖK marjı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Nakit yaratma kapasitesi güçlü.' if diff_pct > 10 else 'Nakit yaratma potansiyeli kısıtlı.'}",
            "current_ratio": f"Cari oran sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Kısa vadeli likidite pozisyonu güçlü.' if val and val > 1.5 else 'Kısa vadeli likidite riski dikkat çekici.' if val and val < 1 else 'Likidite dengede.'}",
            "acid_test_ratio": f"Asit test oranı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Stoksuz likidite gücü yüksek.' if val and val > 1 else 'Stoksuz likidite riski var.'}",
            "debt_ratio": f"Borçlanma oranı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Finansal risk düşük.' if diff_pct < -10 else 'Yüksek borçlanma riski.' if diff_pct > 10 else 'Borçlanma seviyesi dengede.'}",
            "debt_to_equity": f"Borç/Özkaynak oranı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Kaldıraç düşük ve güvenli.' if diff_pct < -10 else 'Kaldıraç yüksek — dikkatli olunmalı.' if diff_pct > 10 else 'Kaldıraç seviyesi dengede.'}",
            "net_debt_to_equity": f"Net Borç/Özkaynak oranı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Net borç seviyesi düşük.' if diff_pct < -10 else 'Net borç yüksek — refinansman riski.' if diff_pct > 10 else 'Net borç seviyesi dengede.'}",
            "asset_turnover": f"Aktif devir hızı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Varlık kullanımı verimli.' if diff_pct > 10 else 'Varlık kullanımında verimlilik artırılabilir.'}",
            "npl_ratio": f"Takipteki kredi oranı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Kredi kalitesi güçlü.' if diff_pct < -10 else 'Kredi kalitesi riskli.' if diff_pct > 10 else 'Kredi kalitesi ortalamada.'}",
            "capital_adequacy": f"Sermaye yeterlilik oranı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Sermaye yapısı güçlü.' if diff_pct > 10 else 'Sermaye yeterliliği düşük.' if diff_pct < -10 else 'Sermaye yapısı dengede.'}",
            "net_interest_margin": f"Net faiz marjı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Faiz geliri performansı güçlü.' if diff_pct > 10 else 'Faiz marjı baskılı.'}",
            "cost_income_ratio": f"Maliyet/Gelir oranı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Operasyonel verimlilik yüksek.' if diff_pct < -10 else 'Gider yönetimi iyileştirilebilir.'}",
            "loan_to_deposit": f"Kredi/Mevduat oranı sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}. {'Likidite yönetimi sağlıklı.' if diff_pct < 10 else 'Likidite baskısı var.'}",
        }

        return interpretations.get(ratio_code, f"Sektör ortalamasına göre %{abs(diff_pct):.1f} {direction}.")

    def _build_executive_summary(self, company, score_card, ratio_cards, sector_position) -> str:
        """Build 1-paragraph executive summary."""
        name = company.name
        ticker = company.ticker
        sector = company.sector_main

        score_val = score_card.get("score_sektor") if score_card else None
        karlilik_val = score_card.get("score_karlilik") if score_card else None
        percentile = score_card.get("percentile_sector") if score_card else None
        rank = sector_position.get("rank") if sector_position else None
        total = sector_position.get("total_companies") if sector_position else None

        parts = [f"{name} ({ticker}), {sector} sektöründe"]

        if score_val:
            if score_val > 70:
                perf = "güçlü bir temel analiz performansı sergiliyor"
            elif score_val > 50:
                perf = "ortalamanın üzerinde bir temel analiz performansı sergiliyor"
            elif score_val > 30:
                perf = "sektör ortalamasında bir performans sergiliyor"
            else:
                perf = "temel analiz kriterlerine göre zayıf bir performans sergiliyor"
            parts.append(f"{perf} (genel puan: {score_val:.1f}/100)")

        if karlilik_val:
            if karlilik_val > 70:
                parts.append(f"kârlılık göstergeleri güçlü (kârlılık puanı: {karlilik_val:.1f}/100)")
            elif karlilik_val < 40:
                parts.append(f"kârlılık göstergeleri zayıf (kârlılık puanı: {karlilik_val:.1f}/100)")

        if rank and total:
            parts.append(f"sektöründe {rank}/{total} sıralamasında")

        if percentile:
            parts.append(f"(%{percentile:.0f} percentilde)")

        # Add key strength or weakness
        top_ratios = sorted(
            [r for r in ratio_cards if r.get("percentile") is not None],
            key=lambda x: x.get("percentile", 0),
            reverse=True
        )
        if top_ratios and top_ratios[0].get("percentile", 0) > 70:
            parts.append(f"Öne çıkan alan: {top_ratios[0]['ratio_name']}.")

        weak_ratios = sorted(
            [r for r in ratio_cards if r.get("percentile") is not None],
            key=lambda x: x.get("percentile", 0)
        )
        if weak_ratios and weak_ratios[0].get("percentile", 0) < 30:
            parts.append(f"Dikkat gerektiren alan: {weak_ratios[0]['ratio_name']}.")

        return ". ".join(parts) + "."

    def _build_financial_health(self, ratio_cards) -> Dict[str, Any]:
        """Build financial health section."""
        health_ratios = [r for r in ratio_cards if r["ratio_code"] in [
            "current_ratio", "acid_test_ratio", "debt_ratio", "debt_to_equity", "net_debt_to_equity"
        ]]

        above = [r for r in health_ratios if r.get("percentile", 50) > 60]
        below = [r for r in health_ratios if r.get("percentile", 50) < 40]

        if len(above) > len(below):
            status = "strong"
            status_text = "Finansal durum güçlü — borçlanma ve likidite göstergeleri sağlıklı."
        elif len(below) > len(above):
            status = "caution"
            status_text = "Finansal durumda dikkat gerektiren alanlar mevcut."
        else:
            status = "neutral"
            status_text = "Finansal durum sektör ortalamasında."

        # Interpretations
        interpretations = []
        for r in health_ratios:
            val = r.get("company_value")
            med = r.get("sector_median")
            diff = r.get("diff_pct", 0)
            if val is not None:
                interpretations.append({
                    "metric": r["ratio_name"],
                    "value": val,
                    "sector_median": med,
                    "diff_pct": diff,
                    "interpretation": r.get("interpretation", ""),
                })

        return {
            "status": status,
            "status_text": status_text,
            "metrics": interpretations,
        }

    def _build_profitability(self, ratio_cards, score_card) -> Dict[str, Any]:
        """Build profitability analysis section."""
        prof_ratios = [r for r in ratio_cards if r["ratio_code"] in [
            "roe", "roa", "gross_margin", "net_margin", "operating_margin", "ebitda_margin",
            "cost_income_ratio", "net_interest_margin"
        ]]

        karlilik_val = score_card.get("score_karlilik") if score_card else None

        metrics = []
        for r in prof_ratios:
            val = r.get("company_value")
            if val is not None:
                # Format as percentage for margin ratios
                if r["ratio_code"] in ["roe", "roa", "gross_margin", "net_margin", "operating_margin", "ebitda_margin", "net_interest_margin"]:
                    display_val = f"%{val*100:.1f}"
                elif r["ratio_code"] == "cost_income_ratio":
                    display_val = f"%{val*100:.1f}"
                else:
                    display_val = f"{val:.2f}"

                metrics.append({
                    "metric": r["ratio_name"],
                    "value": display_val,
                    "raw_value": val,
                    "sector_median": r.get("sector_median"),
                    "percentile": r.get("percentile"),
                    "diff_pct": r.get("diff_pct", 0),
                    "interpretation": r.get("interpretation", ""),
                })

        # Overall assessment
        if karlilik_val:
            if karlilik_val > 70:
                assessment = "Kârlılık performansı sektör üst çeyreğinde — güçlü."
            elif karlilik_val > 50:
                assessment = "Kârlılık performansı ortalamanın üzerinde."
            elif karlilik_val > 30:
                assessment = "Kârlılık performansı sektör ortalamasında."
            else:
                assessment = "Kârlılık performansı düşük — iyileşme gerekiyor."
        else:
            assessment = "Kârlılık değerlendirmesi için yeterli veri mevcut değil."

        return {
            "assessment": assessment,
            "karlilik_score": karlilik_val,
            "metrics": metrics,
        }

    def _build_sector_comparison(self, sector_position, ratio_cards) -> Dict[str, Any]:
        """Build sector comparison section."""
        if not sector_position:
            return {
                "summary": "Sektör karşılaştırma verisi bulunamadı.",
                "rank": None,
                "total": None,
                "percentile": None,
                "above_count": 0,
                "below_count": 0,
            }

        above_count = len(sector_position.get("above_median_ratios", []))
        below_count = len(sector_position.get("below_median_ratios", []))
        total = above_count + below_count

        if total > 0:
            above_pct = (above_count / total) * 100
            if above_pct > 70:
                perf_desc = "sektör ortalamasının üzerinde güçlü bir performans"
            elif above_pct > 50:
                perf_desc = "çoğunlukla sektör ortalamasının üzerinde"
            elif above_pct > 30:
                perf_desc = "sektör ortalamasına yakın bir performans"
            else:
                perf_desc = "çoğunlukla sektör ortalamasının altında"

            summary = f"Sektör karşılaştırmasında {above_count}/{total} oranda {perf_desc}."
        else:
            summary = "Sektör karşılaştırma verisi yetersiz."

        return {
            "summary": summary,
            "rank": sector_position.get("rank"),
            "total": sector_position.get("total_companies"),
            "percentile": sector_position.get("percentile"),
            "above_count": above_count,
            "below_count": below_count,
            "above_ratios": sector_position.get("above_median_ratios", []),
            "below_ratios": sector_position.get("below_median_ratios", []),
        }

    def _build_swot_section(self, swot_data) -> Dict[str, Any]:
        """Build SWOT section for report."""
        return {
            "strengths": swot_data.get("strengths", []),
            "weaknesses": swot_data.get("weaknesses", []),
            "opportunities": swot_data.get("opportunities", []),
            "threats": swot_data.get("threats", []),
        }

    def _build_scenarios(self, score_card, ratio_cards, swot_data) -> Dict[str, Any]:
        """Build optimistic/pessimistic scenario analysis."""
        score_val = score_card.get("score_sektor") if score_card else 50

        # Count strengths and weaknesses
        strengths = swot_data.get("strengths", [])
        weaknesses = swot_data.get("weaknesses", [])
        opportunities = swot_data.get("opportunities", [])
        threats = swot_data.get("threats", [])

        # Optimistic scenario
        opt_factors = []
        if score_val > 60:
            opt_factors.append("Mevcut güçlü temel analiz performansının sürdürülmesi")
        if opportunities:
            opt_factors.append(opportunities[0].get("item", "Sektör fırsatlarının değerlendirilmesi"))
        if strengths:
            opt_factors.append(f"Güçlü yönlerin korunması ({strengths[0].get('item', '')})")

        optimistic = {
            "title": "İyimser Senaryo",
            "probability": "düşük-orta" if score_val > 60 else "düşük",
            "factors": opt_factors[:3] if opt_factors else ["Sektördeki genel iyileşme"],
            "outcome": "Değerlemeye bağlı yukarı potansiyel" if score_val > 50 else "Mevcut seviyenin korunması",
        }

        # Pessimistic scenario
        pess_factors = []
        if score_val < 50:
            pess_factors.append("Mevcut zayıf performansın devam etmesi")
        if threats:
            pess_factors.append(threats[0].get("item", "Piyasa risklerinin realized olma ihtimali"))
        if weaknesses:
            pess_factors.append(f"Zayıf yönlerin derinleşmesi ({weaknesses[0].get('item', '')})")

        pessimistic = {
            "title": "Kötümser Senaryo",
            "probability": "düşük" if score_val > 60 else "orta",
            "factors": pess_factors[:3] if pess_factors else ["Piyasa genelinde risk artışı"],
            "outcome": "Değer kaybı riski" if score_val < 50 else "Mevcut seviyenin altına inme riski",
        }

        return {
            "optimistic": optimistic,
            "pessimistic": pessimistic,
        }

    def _build_watchlist(self, ratio_cards, score_card, sector_position) -> List[Dict[str, str]]:
        """Build watchlist of key metrics to monitor."""
        watchlist = []

        # Flag weak metrics
        for r in ratio_cards:
            pct = r.get("percentile", 50)
            if pct < 30:
                watchlist.append({
                    "metric": r["ratio_name"],
                    "status": "risk",
                    "note": f"Sektör alt çeyreğinde (%{pct} percentile). İzlenmeli.",
                })
            elif pct > 80:
                watchlist.append({
                    "metric": r["ratio_name"],
                    "status": "opportunity",
                    "note": f"Sektör üst çeyreğinde (%{pct} percentile). Güçlü alan.",
                })

        # Score trend
        score_val = score_card.get("score_sektor") if score_card else None
        if score_val and score_val < 40:
            watchlist.append({
                "metric": "Genel Temel Analiz Puanı",
                "status": "risk",
                "note": f"Düşük puan ({score_val:.1f}/100). Yapısal iyileşme gerekiyor.",
            })

        # Sector position
        if sector_position and sector_position.get("rank"):
            rank = sector_position["rank"]
            total = sector_position.get("total_companies", 1)
            if rank > total * 0.7:
                watchlist.append({
                    "metric": "Sektör Sıralaması",
                    "status": "risk",
                    "note": f"{rank}/{total} — sektör alt sıralarında.",
                })

        return watchlist[:8]
