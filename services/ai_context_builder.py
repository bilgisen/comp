"""
HissePro AI Context Builder Service
Generates comprehensive context for AI chatbot (Gemini) integration

Author: Kiro AI Assistant
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, text, func

from models.company import Company
from models.financial import CompanyRatio
from services.sector_benchmarks import SectorBenchmarkService
from services.comparison_service import ComparisonService
from services.trend_analysis import TrendAnalysisService
from core.cache import redis_client

logger = logging.getLogger(__name__)


class ContextType(Enum):
    """Types of AI context that can be generated"""
    BASIC = "basic"                    # Company overview + key ratios
    COMPREHENSIVE = "comprehensive"    # Full analysis with benchmarks
    COMPARISON = "comparison"          # Peer comparison focus
    TREND = "trend"                   # Historical trend focus
    SECTOR = "sector"                 # Sector analysis focus


class AIContextBuilder:
    """
    Builds structured, Turkish-language financial context for AI chatbot
    
    Optimized for Gemini API with proper formatting and disclaimers
    Context includes risk warnings and Turkish regulatory compliance
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.benchmark_service = SectorBenchmarkService(db)
        self.comparison_service = ComparisonService(db)
        self.trend_service = TrendAnalysisService(db)

    async def build_context(
        self, 
        ticker: str,
        context_type: ContextType = ContextType.COMPREHENSIVE,
        period_key: Optional[str] = None,
        cache_ttl: int = 1800  # 30 minutes
    ) -> Dict[str, Any]:
        """
        Build AI context for specified company and context type
        
        Args:
            ticker: Company ticker symbol
            context_type: Type of context to generate
            period_key: Specific period, latest if None
            cache_ttl: Cache time-to-live in seconds
        """
        try:
            # Convert string to Enum if necessary
            if isinstance(context_type, str):
                try:
                    context_type = ContextType(context_type)
                except ValueError:
                    raise ValueError(f"Geçersiz context_type: {context_type}")

            logger.info(f"🤖 Building AI context: {ticker} ({context_type.value})")
            
            # Check cache first
            cache_key = f"ai_context:{ticker}:{context_type.value}:{period_key or 'latest'}"
            cached_context = await redis_client.get(cache_key)
            
            if cached_context:
                logger.debug(f"📊 Cache hit: AI context for {ticker}")
                return cached_context
            
            # Get company info
            company = await self._get_company_info(ticker)
            if not company:
                raise ValueError(f"Şirket bulunamadı: {ticker}")
            
            # Get latest period if not specified
            if not period_key:
                period_key = await self._get_latest_period()
            
            # Build context based on type
            if context_type == ContextType.BASIC:
                context = await self._build_basic_context(company, period_key)
            elif context_type == ContextType.COMPREHENSIVE:
                context = await self._build_comprehensive_context(company, period_key)
            elif context_type == ContextType.COMPARISON:
                context = await self._build_comparison_context(company, period_key)
            elif context_type == ContextType.TREND:
                context = await self._build_trend_context(company, period_key)
            elif context_type == ContextType.SECTOR:
                context = await self._build_sector_context(company, period_key)
            else:
                raise ValueError(f"Desteklenmeyen context tipi: {context_type}")
            
            # Add metadata and disclaimers
            final_context = self._finalize_context(context, ticker, context_type, period_key)
            
            # Cache result
            await redis_client.setex(cache_key, cache_ttl, final_context)
            
            logger.info(f"✅ AI context built: {len(final_context['content'])} chars")
            return final_context
            
        except Exception as e:
            logger.error(f"AI context building failed: {e}", exc_info=True)
            raise

    async def _build_basic_context(
        self, 
        company: Dict[str, Any], 
        period_key: str
    ) -> Dict[str, Any]:
        """Build basic company context with key metrics"""
        
        # Get key ratios
        key_ratios = await self._get_key_ratios(company["ticker"], period_key)
        
        # Get sector benchmarks for key ratios
        sector_data = None
        if key_ratios:
            sector_data = await self.benchmark_service.get_sector_benchmarks(
                company["sector_main"], period_key, list(key_ratios.keys())
            )
        
        content = f"""# {company['company_name']} ({company['ticker']}) - Temel Analiz

## Şirket Bilgileri
- **Sektör:** {company['sector_main']}
- **Piyasa Değeri:** {self._format_market_cap(company.get('market_cap'))}
- **Analiz Dönemi:** {period_key}

## Temel Finansal Rasyolar"""
        
        if key_ratios and sector_data:
            for ratio_code, value in key_ratios.items():
                ratio_name = self._get_ratio_display_name(ratio_code)
                
                # Add sector comparison if available
                benchmark = sector_data.get("benchmarks", {}).get(ratio_code)
                sector_text = ""
                if benchmark and benchmark.get("median_ew"):
                    sector_median = benchmark["median_ew"]
                    vs_sector = "üstünde" if value > sector_median else "altında"
                    sector_text = f" (Sektör ortalaması: {sector_median:.2f}, şirket sektör {vs_sector})"
                
                content += f"\n- **{ratio_name}:** {value:.2f}{sector_text}"
        else:
            content += "\n- Finansal rasyo verisi mevcut değil"
        
        return {"content": content, "type": "basic"}
    async def _build_comprehensive_context(
        self, 
        company: Dict[str, Any], 
        period_key: str
    ) -> Dict[str, Any]:
        """Build comprehensive financial analysis context"""
        
        ticker = company["ticker"]
        
        # Get all company ratios
        all_ratios = await self._get_company_ratios(ticker, period_key)
        
        # Get sector comparison
        sector_comparison = await self.comparison_service.compare_to_sector(
            ticker, period_key
        )
        
        # Get trend analysis (last 6 periods)
        trend_analysis = await self.trend_service.analyze_company_trends(
            ticker, periods=6
        )
        
        content = f"""# {company['company_name']} ({ticker}) - Kapsamlı Finansal Analiz

## Şirket Profili
- **Şirket Adı:** {company['company_name']}
- **Sektör:** {company['sector_main']}
- **Piyasa Değeri:** {self._format_market_cap(company.get('market_cap'))}
- **Analiz Dönemi:** {period_key}
- **Son Güncelleme:** {datetime.now().strftime('%d.%m.%Y %H:%M')}

## Sektör Pozisyonu"""
        
        if sector_comparison and sector_comparison.get("sector_analysis"):
            analysis = sector_comparison["sector_analysis"]
            position_text = self._translate_position(analysis.get("position", "average"))
            
            content += f"""
- **Sektör İçi Konum:** {position_text}
- **Ortalama Persentil:** {analysis.get('average_percentile', 'N/A')}%
- **Güçlü Alanlar:** {', '.join([self._get_ratio_display_name(r) for r in analysis.get('strength_ratios', [])[:3]])}
- **Gelişim Alanları:** {', '.join([self._get_ratio_display_name(r) for r in analysis.get('weakness_ratios', [])[:3]])}"""
        
        # Liquidity analysis
        content += "\n\n## Likidite Analizi"
        liquidity_ratios = self._filter_ratios_by_category(all_ratios, "liquidity")
        content += self._format_ratio_section(
            liquidity_ratios, sector_comparison.get("detailed_comparisons", [])
        )
        
        # Profitability analysis  
        content += "\n\n## Kârlılık Analizi"
        profitability_ratios = self._filter_ratios_by_category(all_ratios, "profitability")
        content += self._format_ratio_section(
            profitability_ratios, sector_comparison.get("detailed_comparisons", [])
        )
        
        # Leverage analysis
        content += "\n\n## Kaldıraç ve Risk Analizi"
        leverage_ratios = self._filter_ratios_by_category(all_ratios, "leverage")
        content += self._format_ratio_section(
            leverage_ratios, sector_comparison.get("detailed_comparisons", [])
        )
        
        # Valuation analysis
        content += "\n\n## Değerleme Rasyoları"
        valuation_ratios = self._filter_ratios_by_category(all_ratios, "valuation")
        content += self._format_ratio_section(
            valuation_ratios, sector_comparison.get("detailed_comparisons", [])
        )
        
        # Trend analysis
        if trend_analysis and trend_analysis.get("trend_summary"):
            content += "\n\n## Trend Analizi"
            summary = trend_analysis["trend_summary"]
            momentum_text = self._translate_momentum(summary.get("overall_momentum", "neutral"))
            
            content += f"""
- **Genel Momentum:** {momentum_text}
- **Momentum Skoru:** {summary.get('momentum_score', 0):.1f}/100
- **İyileşen Rasyolar:** {summary.get('improving_count', 0)} adet
- **Kötüleşen Rasyolar:** {summary.get('declining_count', 0)} adet

### Öne Çıkan Trendler"""
            
            if summary.get("key_improvements"):
                improvements = [self._get_ratio_display_name(r) for r in summary["key_improvements"][:3]]
                content += f"\n- **İyileşme:** {', '.join(improvements)}"
            
            if summary.get("key_deteriorations"):
                deteriorations = [self._get_ratio_display_name(r) for r in summary["key_deteriorations"][:3]]
                content += f"\n- **Kötüleşme:** {', '.join(deteriorations)}"
        
        return {"content": content, "type": "comprehensive"}

    async def _build_comparison_context(
        self, 
        company: Dict[str, Any], 
        period_key: str
    ) -> Dict[str, Any]:
        """Build peer comparison focused context"""
        
        ticker = company["ticker"]
        
        # Get sector peers for comparison
        sector_peers = await self._get_sector_peers(company["sector_main"], ticker, limit=5)
        
        content = f"""# {company['company_name']} - Sektör Karşılaştırması

## Sektör Analizi: {company['sector_main']}

### Sektör Özellikleri"""
        
        # Add sector-specific context
        sector_context = self._get_sector_characteristics(company["sector_main"])
        content += f"\n{sector_context}"
        
        content += f"\n\n### Sektördeki Konumu"
        
        # Get detailed sector comparison
        sector_comparison = await self.comparison_service.compare_to_sector(ticker, period_key)
        
        if sector_comparison:
            content += self._format_sector_comparison_detailed(sector_comparison)
        
        content += f"\n\n### Sektör Rakipleri"
        if sector_peers:
            for peer in sector_peers[:3]:  # Top 3 peers
                content += f"\n- {peer['company_name']} ({peer['ticker']})"
                if peer.get('market_cap'):
                    content += f" - Piyasa Değeri: {self._format_market_cap(peer['market_cap'])}"
        
        return {"content": content, "type": "comparison"}

    async def _build_trend_context(
        self, 
        company: Dict[str, Any], 
        period_key: str
    ) -> Dict[str, Any]:
        """Build historical trend focused context"""
        
        ticker = company["ticker"]
        
        # Get extended trend analysis (8 periods = 2 years)
        trend_analysis = await self.trend_service.analyze_company_trends(
            ticker, periods=8
        )
        
        content = f"""# {company['company_name']} - Tarihsel Trend Analizi

## Finansal Performans Trendi"""
        
        if trend_analysis and trend_analysis.get("trend_summary"):
            summary = trend_analysis["trend_summary"] 
            
            content += f"""
- **Analiz Dönemi:** {trend_analysis.get('analysis_period', {}).get('date_range', {}).get('start', 'N/A')} - {trend_analysis.get('analysis_period', {}).get('date_range', {}).get('end', 'N/A')}
- **Toplam Rasyo:** {summary.get('total_ratios', 0)}
- **Genel Trend:** {self._translate_momentum(summary.get('overall_momentum', 'neutral'))}
- **Momentum Skoru:** {summary.get('momentum_score', 0):.1f}/100"""
            
            # Detailed trend breakdown by category
            detailed_trends = trend_analysis.get("detailed_trends", [])
            
            for category in ["liquidity", "profitability", "leverage", "valuation"]:
                category_trends = [t for t in detailed_trends if t.get("category") == category]
                if category_trends:
                    content += f"\n\n### {self._translate_category(category)} Trendleri"
                    
                    for trend in category_trends[:3]:  # Top 3 per category
                        direction = self._translate_trend_direction(trend.get("direction", ""))
                        content += f"\n- **{trend.get('ratio_name', trend.get('ratio_code'))}:** {direction}"
                        
                        if trend.get("change_1y"):
                            change_pct = trend["change_1y"] * 100
                            change_text = "artış" if change_pct > 0 else "azalış"
                            content += f" (Yıllık %{abs(change_pct):.1f} {change_text})"
        
        return {"content": content, "type": "trend"}
    async def _build_sector_context(
        self, 
        company: Dict[str, Any], 
        period_key: str
    ) -> Dict[str, Any]:
        """Build sector-wide analysis context"""
        
        sector_main = company["sector_main"]
        
        # Get sector benchmarks
        sector_benchmarks = await self.benchmark_service.get_sector_benchmarks(
            sector_main, period_key
        )
        
        # Get sector companies
        sector_companies = await self._get_sector_companies(sector_main)
        
        content = f"""# {sector_main} Sektör Analizi

## Sektör Genel Bakış

### Sektör Karakteristikleri
{self._get_sector_characteristics(sector_main)}

### Sektör İstatistikleri
- **Toplam Şirket Sayısı:** {len(sector_companies)}
- **Analiz Dönemi:** {period_key}
- **Benchmark Güvenilirlik:** {self._assess_sector_benchmark_quality(sector_benchmarks)}"""
        
        if sector_benchmarks and sector_benchmarks.get("benchmarks"):
            content += "\n\n### Sektör Medyan Değerleri"
            
            benchmarks = sector_benchmarks["benchmarks"]
            
            # Group ratios by category
            for category in ["liquidity", "profitability", "leverage", "valuation"]:
                category_benchmarks = {
                    code: data for code, data in benchmarks.items()
                    if self._get_ratio_category(code) == category
                }
                
                if category_benchmarks:
                    content += f"\n\n#### {self._translate_category(category)}"
                    
                    for ratio_code, benchmark in list(category_benchmarks.items())[:4]:  # Top 4 per category
                        ratio_name = self._get_ratio_display_name(ratio_code)
                        median = benchmark.get("median_ew")
                        
                        if median is not None:
                            content += f"\n- **{ratio_name}:** {median:.2f}"
                            
                            # Add quartile range if available
                            p25 = benchmark.get("p25")
                            p75 = benchmark.get("p75") 
                            if p25 is not None and p75 is not None:
                                content += f" (Q1: {p25:.2f}, Q3: {p75:.2f})"
        
        # Top sector companies
        top_companies = sorted(
            sector_companies, 
            key=lambda x: x.get("market_cap", 0) or 0, 
            reverse=True
        )[:5]
        
        if top_companies:
            content += "\n\n### Sektör Liderleri (Piyasa Değeri)"
            for i, comp in enumerate(top_companies, 1):
                market_cap_text = self._format_market_cap(comp.get("market_cap"))
                content += f"\n{i}. {comp['company_name']} ({comp['ticker']}) - {market_cap_text}"
        
        return {"content": content, "type": "sector"}

    def _finalize_context(
        self, 
        context: Dict[str, Any], 
        ticker: str,
        context_type: ContextType, 
        period_key: str
    ) -> Dict[str, Any]:
        """Add metadata and disclaimers to context"""
        
        # Add risk disclaimers
        disclaimers = """

## ⚠️ Önemli Uyarılar ve Yasal Bildirim

### Risk Uyarısı
- Bu analiz sadece bilgilendirme amaçlıdır, yatırım tavsiyesi değildir
- Geçmiş performans gelecekteki sonuçları garanti etmez
- Yatırım kararlarınızı vermeden önce profesyonel danışmanlık alın
- Mali tablolar ve rasyolar gecikmeli veri içerebilir

### Veri Kaynağı ve Güncellik
- Veriler İş Yatırım API'sinden alınmaktadır
- Son güncelleme: """ + datetime.now().strftime('%d.%m.%Y %H:%M') + """
- Analiz dönemi: """ + period_key + """

### Metodoloji
- Sektör karşılaştırmaları F1-F5 filtreli medyan hesaplaması kullanır
- Trend analizcinde linear regresyon ve istatistiksel anlamlılık testleri uygulanır
- Tüm rasyolar TTM (son 12 ay) basis üzerinden hesaplanır

### SPK Uyum Bildirimi
Bu içerik SPK mevzuatına uygun olarak hazırlanmış olup, yatırım danışmanlığı faaliyeti kapsamında değildir."""
        
        return {
            "ticker": ticker,
            "context_type": context_type.value,
            "period_key": period_key,
            "generated_at": datetime.utcnow().isoformat(),
            "content": context["content"] + disclaimers,
            "metadata": {
                "content_length": len(context["content"]),
                "language": "tr",
                "format": "markdown",
                "version": "2.0"
            }
        }

    # Helper methods for data access
    async def _get_company_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get company information"""
        query = select(Company).where(Company.ticker == ticker)
        result = await self.db.execute(query)
        company = result.scalar_one_or_none()
        
        if not company:
            return None
            
        return {
            "ticker": company.ticker,
            "company_name": company.name,
            "sector_main": company.sector_main,
            "market_cap": float(company.market_cap) if company.market_cap else None,
            "is_active": company.is_active
        }

    async def _get_company_ratios(self, ticker: str, period_key: str) -> Dict[str, float]:
        """Get all company ratios for period"""
        query = select(CompanyRatio).where(
            and_(
                CompanyRatio.ticker == ticker,
                CompanyRatio.period_key == period_key
            )
        )
        result = await self.db.execute(query)
        ratios = result.scalars().all()
        
        return {
            ratio.ratio_code: float(ratio.ratio_value) if ratio.ratio_value else None
            for ratio in ratios
        }

    async def _get_key_ratios(self, ticker: str, period_key: str) -> Dict[str, float]:
        """Get key ratios for basic context"""
        all_ratios = await self._get_company_ratios(ticker, period_key)
        
        # Key ratios for basic analysis
        key_ratio_codes = [
            "current_ratio", "roe", "roa", "debt_to_equity", 
            "net_margin", "pe_ratio", "pb_ratio"
        ]
        
        return {code: value for code, value in all_ratios.items() if code in key_ratio_codes}

    async def _get_latest_period(self) -> str:
        """Get latest available period"""
        query = text("SELECT period_key FROM company_ratios ORDER BY created_at DESC LIMIT 1")
        result = await self.db.execute(query)
        row = result.fetchone()
        return row.period_key if row else "2026Q1"

    async def _get_sector_peers(
        self, 
        sector_main: str, 
        exclude_ticker: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get sector peer companies"""
        query = select(Company).where(
            and_(
                Company.sector_main == sector_main,
                Company.ticker != exclude_ticker,
                Company.is_active == True
            )
        ).order_by(Company.market_cap.desc()).limit(limit)
        
        result = await self.db.execute(query)
        companies = result.scalars().all()
        
        return [
            {
                "ticker": company.ticker,
                "company_name": company.name,
                "market_cap": float(company.market_cap) if company.market_cap else None
            }
            for company in companies
        ]

    async def _get_sector_companies(self, sector_main: str) -> List[Dict[str, Any]]:
        """Get all companies in sector"""
        query = select(Company).where(
            and_(
                Company.sector_main == sector_main,
                Company.is_active == True
            )
        )
        
        result = await self.db.execute(query)
        companies = result.scalars().all()
        
        return [
            {
                "ticker": company.ticker,
                "company_name": company.name,
                "market_cap": float(company.market_cap) if company.market_cap else None
            }
            for company in companies
        ]
    # Helper methods for formatting and translation
    def _format_market_cap(self, market_cap: Optional[float]) -> str:
        """Format market cap in Turkish"""
        if not market_cap:
            return "Belirtilmemiş"
        
        if market_cap >= 1_000_000_000:
            return f"{market_cap/1_000_000_000:.1f} Milyar TL"
        elif market_cap >= 1_000_000:
            return f"{market_cap/1_000_000:.1f} Milyon TL"
        else:
            return f"{market_cap/1_000:.1f} Bin TL"

    def _get_ratio_display_name(self, ratio_code: str) -> str:
        """Get Turkish ratio names"""
        display_names = {
            "current_ratio": "Cari Oran",
            "acid_test_ratio": "Asit Test Oranı",
            "gross_margin": "Brüt Kar Marjı",
            "ebitda_margin": "FAVÖK Marjı", 
            "net_margin": "Net Kar Marjı",
            "roe": "Özsermaye Karlılığı (ROE)",
            "roa": "Aktif Karlılığı (ROA)",
            "debt_ratio": "Borçlanma Oranı",
            "debt_to_equity": "Borç/Özsermaye Oranı",
            "pe_ratio": "F/K Oranı",
            "pb_ratio": "PD/DD Oranı",
            "ev_ebitda": "FD/FAVÖK Oranı",
            "net_interest_margin": "Net Faiz Marjı",
            "loan_to_deposit": "Kredi/Mevduat Oranı",
            "npl_ratio": "Takipteki Kredi Oranı (NPL)",
            "capital_adequacy": "Sermaye Yeterlilik Oranı (CAR)",
            "cost_income_ratio": "Maliyet/Gelir Oranı",
            "loss_ratio": "Hasar Oranı",
            "expense_ratio": "Gider Oranı",
            "combined_ratio": "Birleşik Oran",
            "nav_discount": "Net Aktif Değer (NAD) İskontosu",
            "rental_yield": "Kira Getirisi"
        }
        return display_names.get(ratio_code, ratio_code.replace("_", " ").title())

    def _get_ratio_category(self, ratio_code: str) -> str:
        """Get ratio category"""
        liquidity_ratios = ["current_ratio", "acid_test_ratio", "cash_ratio"]
        profitability_ratios = [
            "gross_margin", "ebitda_margin", "net_margin", "roe", "roa",
            "loss_ratio", "combined_ratio", "rental_yield"
        ]
        leverage_ratios = ["debt_ratio", "debt_to_equity", "interest_coverage"]
        valuation_ratios = ["pe_ratio", "pb_ratio", "ev_ebitda", "price_to_sales", "nav_discount"]
        efficiency_ratios = [
            "asset_turnover", "inventory_turnover", "receivables_turnover", 
            "expense_ratio", "cost_income_ratio"
        ]
        banking_ratios = ["net_interest_margin", "loan_to_deposit", "npl_ratio", "capital_adequacy"]
        
        if ratio_code in liquidity_ratios:
            return "liquidity"
        elif ratio_code in profitability_ratios:
            return "profitability"
        elif ratio_code in leverage_ratios:
            return "leverage"
        elif ratio_code in valuation_ratios:
            return "valuation"
        elif ratio_code in efficiency_ratios:
            return "efficiency"
        elif ratio_code in banking_ratios:
            return "banking"
        else:
            return "other"

    def _filter_ratios_by_category(
        self, 
        ratios: Dict[str, float], 
        category: str
    ) -> Dict[str, float]:
        """Filter ratios by category"""
        return {
            code: value for code, value in ratios.items()
            if self._get_ratio_category(code) == category and value is not None
        }

    def _format_ratio_section(
        self, 
        ratios: Dict[str, float],
        sector_comparisons: List[Dict[str, Any]]
    ) -> str:
        """Format ratio section with sector comparison"""
        if not ratios:
            return "\n- Bu kategoride mevcut veri bulunmuyor"
        
        content = ""
        
        # Create lookup for sector comparisons
        sector_lookup = {
            comp["ratio_code"]: comp for comp in sector_comparisons
            if comp["ratio_code"] in ratios
        }
        
        for ratio_code, value in ratios.items():
            ratio_name = self._get_ratio_display_name(ratio_code)
            content += f"\n- **{ratio_name}:** {value:.2f}"
            
            # Add sector context if available
            sector_comp = sector_lookup.get(ratio_code)
            if sector_comp:
                percentile = sector_comp.get("percentile")
                interpretation = sector_comp.get("interpretation", "")
                
                if percentile is not None:
                    content += f" ({percentile:.0f}. persentil - {self._translate_interpretation(interpretation)})"
        
        return content

    def _format_sector_comparison_detailed(self, sector_comparison: Dict[str, Any]) -> str:
        """Format detailed sector comparison"""
        if not sector_comparison or not sector_comparison.get("sector_analysis"):
            return "\n- Sektör karşılaştırma verisi mevcut değil"
        
        analysis = sector_comparison["sector_analysis"]
        
        content = f"""
- **Sektör Pozisyonu:** {self._translate_position(analysis.get('position', 'average'))}
- **Ortalama Persentil:** {analysis.get('average_percentile', 'N/A')}%"""
        
        quartile_dist = analysis.get("quartile_distribution", {})
        if quartile_dist:
            content += f"""
- **Çeyreklik Dağılımı:** Q1: {quartile_dist.get('q1', 0)}, Q2: {quartile_dist.get('q2', 0)}, Q3: {quartile_dist.get('q3', 0)}, Q4: {quartile_dist.get('q4', 0)} rasyo"""
        
        return content

    def _get_sector_characteristics(self, sector_main: str) -> str:
        """Get sector-specific characteristics description"""
        
        characteristics = {
            "Bankacılık & Finans": """
Türkiye bankacılık sektörü yüksek regulasyon altında faaliyet gösterir. Temel performans göstergeleri net faiz marjı, 
kredi kalitesi ve sermaye yeterliliği oranlarıdır. BDDK düzenlemelerine tabi olup, Basel III standartlarını uygular.""",
            
            "Teknoloji & İletişim": """
Yüksek büyüme potansiyeli olan sektör. Ar-Ge yoğun yapısı nedeniyle kârlılık rasyoları volatil olabilir. 
Değerleme oranları geleneksel sektörlerden yüksek seviyelerde işlem görebilir.""",
            
            "Enerji & Altyapı": """
Sermaye yoğun sektör. Yüksek sabit varlık seviyesi ve uzun vadeli proje finansmanı nedeniyle borçlanma oranları 
diğer sektörlerden yüksek olabilir. Düzenleyici otoritelerle yakın ilişki içindedir.""",
            
            "GYO": """
Gayrimenkul Yatırım Ortaklıkları özel bir yapıya sahiptir. NAV (Net Varlık Değeri) bazlı değerleme yaygındır. 
Kira gelirleri odaklı iş modeli ve vergi avantajları nedeniyle yüksek temettü ödeme eğilimindedir."""
        }
        
        return characteristics.get(sector_main, "Genel sanayi sektörü karakteristikleri geçerlidir.")

    def _assess_sector_benchmark_quality(self, sector_benchmarks: Dict[str, Any]) -> str:
        """Assess sector benchmark data quality"""
        if not sector_benchmarks or not sector_benchmarks.get("benchmarks"):
            return "Yetersiz"
        
        benchmarks = sector_benchmarks["benchmarks"]
        high_reliability = len([b for b in benchmarks.values() if b.get("reliability") == "HIGH"])
        total_benchmarks = len(benchmarks)
        
        if high_reliability / total_benchmarks >= 0.7:
            return "Yüksek"
        elif high_reliability / total_benchmarks >= 0.4:
            return "Orta"
        else:
            return "Düşük"

    # Translation helper methods
    def _translate_position(self, position: str) -> str:
        """Translate sector position to Turkish"""
        translations = {
            "sector_leader": "Sektör Lideri",
            "above_average": "Ortalamanın Üstünde",
            "average": "Sektör Ortalaması",
            "below_average": "Ortalamanın Altında",
            "underperformer": "Zayıf Performans"
        }
        return translations.get(position, position)

    def _translate_momentum(self, momentum: str) -> str:
        """Translate momentum to Turkish"""
        translations = {
            "positive": "Pozitif Momentum",
            "negative": "Negatif Momentum", 
            "neutral": "Nötr/Karışık"
        }
        return translations.get(momentum, momentum)

    def _translate_category(self, category: str) -> str:
        """Translate ratio category to Turkish"""
        translations = {
            "liquidity": "Likidite",
            "profitability": "Kârlılık",
            "leverage": "Kaldıraç",
            "valuation": "Değerleme",
            "efficiency": "Verimlilik",
            "banking": "Bankacılık"
        }
        return translations.get(category, category)

    def _translate_trend_direction(self, direction: str) -> str:
        """Translate trend direction to Turkish"""
        translations = {
            "strongly_improving": "Güçlü İyileşme",
            "improving": "İyileşme Trendi",
            "stable": "Sabit",
            "declining": "Kötüleşme Trendi",
            "strongly_declining": "Güçlü Kötüleşme",
            "volatile": "Değişken"
        }
        return translations.get(direction, direction)

    def _translate_interpretation(self, interpretation: str) -> str:
        """Translate percentile interpretation to Turkish"""
        translations = {
            "exceptional": "İstisnaî",
            "strong": "Güçlü",
            "above_average": "Ortalamanın Üstünde",
            "average": "Ortalama",
            "below_average": "Ortalamanın Altında",
            "weak": "Zayıf",
            "concerning": "Endişe Verici"
        }
        return translations.get(interpretation, interpretation)