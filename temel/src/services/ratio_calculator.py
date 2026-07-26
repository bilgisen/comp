import math
from typing import Optional, List, Dict, Callable
from dataclasses import dataclass

@dataclass
class RatioConfig:
    code: str
    formula: Callable
    type: str
    description: str = ""
    category: str = ""

@dataclass
class CalculationResult:
    ratio_code: str
    value: Optional[float]
    success: bool
    error: Optional[str] = None
    calculation_method: Optional[str] = None
    data_quality_score: Optional[float] = None

FINANCIAL_GROUPS = {
    "Bankacılık": "UFRS_K",
    "Sigorta": "UFRS_S",
    "Fin.Kiralama ve Faktoring": "UFRS_F",
    "GYO": "UFRS_K"
}

ECONOMIC_BOUNDS = {
    "current_ratio": (0.1, 15.0),
    "acid_test_ratio": (0.05, 12.0),
    "debt_to_equity": (-2.0, 25.0),
    "debt_ratio": (0.0, 15.0),
    "gross_margin": (-0.50, 0.95),
    "ebitda_margin": (-0.50, 0.80),
    "net_margin": (-2.00, 0.60),
    "roe": (-1.00, 1.50),
    "roa": (-0.30, 0.40),
    "pe_ratio": (0.0, 150.0),
    "ev_ebitda": (0.0, 60.0),
    "pb_ratio": (0.0, 20.0),
}

class RatioCalculator:
    DEFAULT_RATIOS = {
        "current_ratio": RatioConfig("current_ratio",
            lambda d: d.get("current_assets", 0) / d.get("current_liabilities", 1) if d.get("current_liabilities") else None,
            "instant", "Cari Oran = Dönen Varlıklar / Kısa Vadeli Yükümlülükler", "liquidity"),
        "acid_test_ratio": RatioConfig("acid_test_ratio",
            lambda d: (d.get("current_assets", 0) - d.get("inventories", 0)) / d.get("current_liabilities", 1) if d.get("current_liabilities") else None,
            "instant", "Asit Test Oranı = (Dönen Varlıklar - Stoklar) / Kısa Vadeli Yükümlülükler", "liquidity"),
        "debt_to_equity": RatioConfig("debt_to_equity",
            lambda d: d.get("total_debt", 0) / d.get("shareholders_equity", 1) if d.get("shareholders_equity") else None,
            "instant", "Borç/Özkaynak = Toplam Borç / Özkaynaklar", "leverage"),
        "debt_ratio": RatioConfig("debt_ratio",
            lambda d: d.get("total_liabilities", 0) / d.get("total_assets", 1) if d.get("total_assets") else None,
            "instant", "Borçlanma Oranı = Toplam Yükümlülükler / Toplam Varlıklar", "leverage"),
        "gross_margin": RatioConfig("gross_margin",
            lambda d: d.get("gross_profit_ttm", 0) / d.get("revenue_ttm", 1) if d.get("revenue_ttm") else None,
            "ttm", "Brüt Kâr Marjı = Brüt Kâr (TTM) / Satışlar (TTM)", "profitability"),
        "operating_margin": RatioConfig("operating_margin",
            lambda d: d.get("operating_income_ttm", 0) / d.get("revenue_ttm", 1) if d.get("revenue_ttm") else None,
            "ttm", "Faaliyet Kârı Marjı = Faaliyet Kârı (TTM) / Satışlar (TTM)", "profitability"),
        "net_margin": RatioConfig("net_margin",
            lambda d: d.get("net_income_ttm", 0) / d.get("revenue_ttm", 1) if d.get("revenue_ttm") else None,
            "ttm", "Net Kâr Marjı = Net Kâr (TTM) / Satışlar (TTM)", "profitability"),
        "ebitda_margin": RatioConfig("ebitda_margin",
            lambda d: d.get("ebitda_ttm", 0) / d.get("revenue_ttm", 1) if d.get("revenue_ttm") else None,
            "ttm", "FAVÖK Marjı = FAVÖK (TTM) / Satışlar (TTM)", "profitability"),
        "roe": RatioConfig("roe",
            lambda d: d.get("net_income_ttm", 0) / d.get("shareholders_equity_avg", 1) if d.get("shareholders_equity_avg") else None,
            "ttm", "Özkaynak Kârlılığı = Net Kâr (TTM) / Ortalama Özkaynaklar", "profitability"),
        "roa": RatioConfig("roa",
            lambda d: d.get("net_income_ttm", 0) / d.get("total_assets_avg", 1) if d.get("total_assets_avg") else None,
            "ttm", "Aktif Kârlılığı = Net Kâr (TTM) / Ortalama Toplam Aktif", "profitability"),
        "pe_ratio": RatioConfig("pe_ratio",
            lambda d: d.get("market_cap", 0) / d.get("net_income_ttm", 1) if d.get("net_income_ttm") and d.get("net_income_ttm") > 0 else None,
            "ttm", "F/K Oranı = Piyasa Değeri / Net Kâr (TTM)", "valuation"),
        "pb_ratio": RatioConfig("pb_ratio",
            lambda d: d.get("market_cap", 0) / d.get("shareholders_equity", 1) if d.get("shareholders_equity") else None,
            "instant", "PD/DD Oranı = Piyasa Değeri / Defter Değeri", "valuation"),
        "ev_ebitda": RatioConfig("ev_ebitda",
            lambda d: (d.get("market_cap", 0) + d.get("net_debt", 0)) / d.get("ebitda_ttm", 1) if d.get("ebitda_ttm") and d.get("ebitda_ttm") > 0 else None,
            "ttm", "FD/FAVÖK = (Piyasa Değeri + Net Borç) / FAVÖK (TTM)", "valuation"),
        "asset_turnover": RatioConfig("asset_turnover",
            lambda d: d.get("revenue_ttm", 0) / d.get("total_assets_avg", 1) if d.get("total_assets_avg") else None,
            "ttm", "Aktif Devir Hızı = Satışlar (TTM) / Ortalama Toplam Aktif", "efficiency"),
    }

    BANKING_RATIOS = {
        "net_interest_margin": RatioConfig("net_interest_margin",
            lambda d: d.get("net_interest_income_ttm", 0) / d.get("total_assets_avg", 1) if d.get("total_assets_avg") else None,
            "ttm", "Net Faiz Marjı = Net Faiz Geliri (TTM) / Ortalama Toplam Aktif", "profitability"),
        "loan_to_deposit": RatioConfig("loan_to_deposit",
            lambda d: d.get("gross_loans", 0) / d.get("deposits", 1) if d.get("deposits") else None,
            "instant", "Kredi/Mevduat Oranı = Brüt Krediler / Mevduat", "banking"),
        "npl_ratio": RatioConfig("npl_ratio",
            lambda d: d.get("non_performing_loans", 0) / d.get("gross_loans", 1) if d.get("gross_loans") else None,
            "instant", "Takipteki Kredi Oranı = Takipteki Krediler / Brüt Krediler", "asset_quality"),
        "cost_income_ratio": RatioConfig("cost_income_ratio",
            lambda d: d.get("operating_expenses_ttm", 0) / d.get("total_operating_income_ttm", 1) if d.get("total_operating_income_ttm") else None,
            "ttm", "Maliyet/Gelir Oranı = Faaliyet Giderleri (TTM) / Toplam Faaliyet Geliri (TTM)", "efficiency"),
    }

    INSURANCE_RATIOS = {
        "loss_ratio": RatioConfig("loss_ratio",
            lambda d: abs(d.get("net_claims_incurred_ttm", 0)) / d.get("net_premium_income_ttm", 1) if d.get("net_premium_income_ttm") else None,
            "ttm", "Hasar Oranı = Net Hasar Giderleri (TTM) / Kazanılmış Net Primler (TTM)", "profitability"),
        "expense_ratio": RatioConfig("expense_ratio",
            lambda d: abs(d.get("operating_expenses_ttm", 0)) / d.get("net_premium_income_ttm", 1) if d.get("net_premium_income_ttm") else None,
            "ttm", "Gider Oranı = Faaliyet Giderleri (TTM) / Kazanılmış Net Primler (TTM)", "efficiency"),
        "combined_ratio": RatioConfig("combined_ratio",
            lambda d: (abs(d.get("net_claims_incurred_ttm", 0)) + abs(d.get("operating_expenses_ttm", 0))) / d.get("net_premium_income_ttm", 1) if d.get("net_premium_income_ttm") else None,
            "ttm", "Birleşik Oran = Hasar Oranı + Gider Oranı (TTM)", "profitability"),
    }

    GYO_RATIOS = {
        "nav_discount": RatioConfig("nav_discount",
            lambda d: 1.0 - (d.get("market_cap", 0) / d.get("shareholders_equity", 1)) if d.get("shareholders_equity") else None,
            "instant", "Net Aktif Değer İskontosu = 1 - (Piyasa Değeri / Özkaynaklar)", "valuation"),
        "rental_yield": RatioConfig("rental_yield",
            lambda d: d.get("revenue_ttm", 0) / d.get("total_assets", 1) if d.get("total_assets") else None,
            "ttm", "Kira Getirisi = Hasılat (TTM) / Toplam Varlıklar", "profitability"),
    }

    SECTOR_RATIOS = {
        "Bankacılık & Finans": {**BANKING_RATIOS, "roe": DEFAULT_RATIOS["roe"], "roa": DEFAULT_RATIOS["roa"]},
        "Sigorta": {**INSURANCE_RATIOS, "roe": DEFAULT_RATIOS["roe"], "roa": DEFAULT_RATIOS["roa"],
                    "pe_ratio": DEFAULT_RATIOS["pe_ratio"], "pb_ratio": DEFAULT_RATIOS["pb_ratio"]},
        "GYO": {**GYO_RATIOS, **{k: v for k, v in DEFAULT_RATIOS.items() if k not in ["current_ratio", "acid_test_ratio"]}},
        "Fin.Kiralama ve Faktoring": {**DEFAULT_RATIOS},
        "_default": DEFAULT_RATIOS
    }

    def _derive_financial_data(self, statements: List[dict], market_cap: Optional[float] = None) -> dict:
        data = {}
        for stmt in statements:
            semantic = stmt.get("semantic_name") or stmt.get("item_desc_tr")
            if semantic and stmt.get("value_try") is not None:
                data[semantic] = float(stmt["value_try"])
        if "total_assets" in data and "shareholders_equity" in data:
            data["total_liabilities"] = data.get("total_liabilities", data["total_assets"] - data["shareholders_equity"])
        data["total_debt"] = data.get("total_debt", data.get("short_term_borrowings", 0) + data.get("long_term_borrowings", 0))
        data["net_debt"] = data.get("net_debt", data["total_debt"] - data.get("cash_and_equivalents", 0))
        data["ebitda"] = data.get("ebitda", data.get("operating_income", 0))
        return data

    def _ttm_values(self, period_groups: dict) -> dict:
        ttm = {}
        sorted_periods = sorted(period_groups.keys(), reverse=True)
        if len(sorted_periods) >= 4:
            last_4 = sorted_periods[:4]
            for item in ["revenue", "gross_profit", "operating_income", "net_income", "ebitda",
                          "net_interest_income", "operating_expenses", "net_claims_incurred", "net_premium_income"]:
                total, count = 0, 0
                for pk in last_4:
                    if item in period_groups[pk]:
                        total += period_groups[pk][item]
                        count += 1
                if count >= 3:
                    ttm[f"{item}_ttm"] = total
        return ttm

    def _average_values(self, period_groups: dict) -> dict:
        avg = {}
        sorted_periods = sorted(period_groups.keys(), reverse=True)
        if len(sorted_periods) >= 2:
            cur = period_groups[sorted_periods[0]]
            prev = period_groups[sorted_periods[1]]
            for item in ["total_assets", "shareholders_equity", "inventories", "accounts_receivable"]:
                if item in cur and item in prev:
                    avg[f"{item}_avg"] = (cur[item] + prev[item]) / 2
        return avg

    def calculate(self, ticker: str, statements: List[dict],
                  sector_main: str, market_cap: Optional[float] = None,
                  period_key: Optional[str] = None) -> List[CalculationResult]:
        if not statements:
            return [CalculationResult("error", None, False, "No financial data")]
        sector_ratios = self.SECTOR_RATIOS.get(sector_main, self.SECTOR_RATIOS["_default"])
        period_groups = {}
        for stmt in statements:
            pk = stmt.get("period_key")
            if pk not in period_groups:
                period_groups[pk] = {}
            semantic = stmt.get("semantic_name") or stmt.get("item_desc_tr")
            if semantic and stmt.get("value_try") is not None:
                period_groups[pk][semantic] = float(stmt["value_try"])
        if not period_key:
            period_key = sorted(period_groups.keys(), reverse=True)[0] if period_groups else None
            if not period_key:
                return [CalculationResult("error", None, False, "No periods found")]
        financial_data = self._derive_financial_data(
            [s for s in statements if s.get("period_key") == period_key],
            market_cap
        )
        financial_data.update(self._ttm_values(period_groups))
        financial_data.update(self._average_values(period_groups))
        if market_cap is not None:
            financial_data["market_cap"] = market_cap
        results = []
        for code, config in sector_ratios.items():
            try:
                value = config.formula(financial_data)
                if value is not None and math.isfinite(value):
                    quality = self._assess_quality(config, financial_data)
                    results.append(CalculationResult(code, value, True,
                        calculation_method=config.description, data_quality_score=quality))
                else:
                    results.append(CalculationResult(code, None, False, "Missing data or invalid result"))
            except Exception as e:
                results.append(CalculationResult(code, None, False, str(e)))
        return results

    def _assess_quality(self, config: RatioConfig, data: dict) -> float:
        code = config.formula.__code__
        fields = list(dict.fromkeys(
            name for name in code.co_names
            if name not in ('get', 'abs', 'max', 'min', 'float', 'int', 'str', 'None', 'True', 'False')
        ))
        if not fields:
            return 1.0
        missing = sum(1 for f in fields if f not in data or data.get(f) is None)
        quality = (len(fields) - missing) / len(fields)
        if config.type == "ttm":
            quality *= 0.95
        return round(quality, 2)
