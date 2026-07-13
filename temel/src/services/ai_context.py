from typing import Optional, List
from datetime import datetime
from db.client import D1Client
from models.company import CompanyModel
from models.financial import FinancialModel
from models.metrics import MetricsModel

RATIO_NAMES = {
    "current_ratio": "Cari Oran", "acid_test_ratio": "Asit Test Oranı",
    "debt_to_equity": "Borç/Özkaynak", "debt_ratio": "Borçlanma Oranı",
    "gross_margin": "Brüt Kâr Marjı", "operating_margin": "Faaliyet Kâr Marjı",
    "net_margin": "Net Kâr Marjı", "ebitda_margin": "FAVÖK Marjı",
    "roe": "Özkaynak Kârlılığı (ROE)", "roa": "Aktif Kârlılığı (ROA)",
    "pe_ratio": "F/K Oranı", "pb_ratio": "PD/DD Oranı",
    "ev_ebitda": "FD/FAVÖK", "asset_turnover": "Aktif Devir Hızı",
    "net_interest_margin": "Net Faiz Marjı", "loan_to_deposit": "Kredi/Mevduat",
    "npl_ratio": "Takipteki Kredi Oranı", "cost_income_ratio": "Maliyet/Gelir",
    "loss_ratio": "Hasar Oranı", "expense_ratio": "Gider Oranı",
    "combined_ratio": "Birleşik Oran", "nav_discount": "NAD İskontosu",
    "rental_yield": "Kira Getirisi"
}

class AIContextBuilder:
    def __init__(self, db: D1Client, cache):
        self.db = db
        self.cache = cache
        self.company_model = CompanyModel(db)
        self.financial_model = FinancialModel(db)
        self.metrics_model = MetricsModel(db)

    async def build_basic_context(self, ticker: str, period_key: Optional[str] = None) -> dict:
        company = await self.company_model.get_by_ticker(ticker)
        if not company:
            return {"error": f"Company {ticker} not found"}
        if not period_key:
            period_key = await self.financial_model.get_latest_period(ticker)
        ratios = await self.financial_model.get_ratios(ticker, period_key)
        metrics = await self.metrics_model.get_by_ticker(ticker)
        content = f"# {company['name']} ({ticker}) - Temel Analiz\n\n"
        content += f"## Şirket Bilgileri\n"
        content += f"- **Sektör:** {company['sector_main']}\n"
        if metrics and metrics.get('market_cap'):
            content += f"- **Piyasa Değeri:** {self._fmt_mcap(metrics['market_cap'])}\n"
        if metrics and metrics.get('last_price'):
            content += f"- **Son Fiyat:** {metrics['last_price']} TL\n"
        content += f"- **Analiz Dönemi:** {period_key}\n\n"
        content += "## Temel Finansal Rasyolar\n"
        if ratios:
            for r in ratios:
                name = RATIO_NAMES.get(r["ratio_code"], r["ratio_code"])
                val = r["ratio_value"]
                if val is not None:
                    content += f"- **{name}:** {val:.2f}\n"
        else:
            content += "- Finansal rasyo verisi mevcut değil\n"
        return self._finalize(ticker, period_key, content, "basic")

    async def build_comprehensive_context(self, ticker: str, period_key: Optional[str] = None) -> dict:
        company = await self.company_model.get_by_ticker(ticker)
        if not company:
            return {"error": f"Company {ticker} not found"}
        if not period_key:
            period_key = await self.financial_model.get_latest_period(ticker)
        ratios = await self.financial_model.get_ratios(ticker, period_key)
        metrics = await self.metrics_model.get_by_ticker(ticker)
        content = f"# {company['name']} ({ticker}) - Kapsamlı Finansal Analiz\n\n"
        content += f"## Şirket Profili\n"
        content += f"- **Şirket:** {company['name']}\n- **Sektör:** {company['sector_main']}\n"
        if metrics and metrics.get('market_cap'):
            content += f"- **Piyasa Değeri:** {self._fmt_mcap(metrics['market_cap'])}\n"
        content += f"- **Analiz Dönemi:** {period_key}\n\n"
        categories = {"liquidity": "Likidite Analizi", "profitability": "Kârlılık Analizi",
                       "leverage": "Kaldıraç ve Risk Analizi", "valuation": "Değerleme Rasyoları",
                       "efficiency": "Verimlilik Analizi", "banking": "Bankacılık Rasyoları",
                       "asset_quality": "Aktif Kalitesi"}
        cat_ratios = {}
        if ratios:
            for r in ratios:
                cat = self._get_category(r["ratio_code"])
                if cat not in cat_ratios:
                    cat_ratios[cat] = []
                cat_ratios[cat].append(r)
        for cat, title in categories.items():
            if cat in cat_ratios and cat_ratios[cat]:
                content += f"\n## {title}\n"
                for r in cat_ratios[cat]:
                    name = RATIO_NAMES.get(r["ratio_code"], r["ratio_code"])
                    val = r["ratio_value"]
                    if val is not None:
                        content += f"- **{name}:** {val:.2f}\n"
        return self._finalize(ticker, period_key, content, "comprehensive")

    def _get_category(self, ratio_code: str) -> str:
        cat_map = {"current_ratio": "liquidity", "acid_test_ratio": "liquidity",
                   "debt_to_equity": "leverage", "debt_ratio": "leverage", "net_debt_to_equity": "leverage",
                   "gross_margin": "profitability", "operating_margin": "profitability", "net_margin": "profitability",
                   "ebitda_margin": "profitability", "roe": "profitability", "roa": "profitability",
                   "pe_ratio": "valuation", "pb_ratio": "valuation", "ev_ebitda": "valuation", "nav_discount": "valuation",
                   "asset_turnover": "efficiency", "net_interest_margin": "banking", "loan_to_deposit": "banking",
                   "cost_income_ratio": "efficiency", "loss_ratio": "profitability", "expense_ratio": "efficiency",
                   "combined_ratio": "profitability", "npl_ratio": "asset_quality", "rental_yield": "profitability"}
        return cat_map.get(ratio_code, "other")

    def _fmt_mcap(self, mcap):
        if mcap >= 1_000_000_000:
            return f"{mcap / 1_000_000_000:.1f} Milyar TL"
        elif mcap >= 1_000_000:
            return f"{mcap / 1_000_000:.1f} Milyon TL"
        return f"{mcap / 1_000:.1f} Bin TL"

    def _finalize(self, ticker: str, period_key: str, content: str, ctx_type: str) -> dict:
        now = datetime.utcnow().strftime("%d.%m.%Y %H:%M")
        disclaimers = f"""

## ⚠️ Önemli Uyarılar
- Bu analiz sadece bilgilendirme amaçlıdır, yatırım tavsiyesi değildir
- Geçmiş performans gelecekteki sonuçları garanti etmez
- Yatırım kararlarınızı vermeden önce profesyonel danışmanlık alın

### Veri Kaynağı ve Güncellik
- Veriler İş Yatırım API'sinden alınmaktadır
- Son güncelleme: {now}
- Analiz dönemi: {period_key}

### SPK Uyum Bildirimi
Bu içerik SPK mevzuatına uygun olarak hazırlanmış olup, yatırım danışmanlığı faaliyeti kapsamında değildir."""
        return {
            "ticker": ticker,
            "context_type": ctx_type,
            "period_key": period_key,
            "generated_at": datetime.utcnow().isoformat(),
            "content": content + disclaimers,
            "metadata": {"content_length": len(content), "language": "tr", "format": "markdown", "version": "1.0"}
        }
