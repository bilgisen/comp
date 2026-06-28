"""
İş Yatırım Item Code to Semantic Name Mapping Service
"""

import logging
from typing import Dict, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.financial import ItemCodeMapping

logger = logging.getLogger(__name__)


class ItemCodeMapper:
    """Maps İş Yatırım API item codes to semantic field names"""
    
    # UFRS_K (Banking) mappings based on GARAN analysis
    UFRS_K_MAPPINGS = {
        # BALANCE SHEET - ASSETS
        "1Z": "total_assets",
        "1A": "cash_and_cb",                    # Nakit + Merkez Bankası
        "1AC": "banks_correspondent",           # Muhabir bankalar
        "1AF": "gross_loans",                   # Brüt krediler
        "1AFD": "non_performing_loans",         # Takipteki krediler
        "1AL": "finance_lease_receivables",     # Finansal kiralama alacakları
        "1AN": "tangible_assets",               # Maddi duran varlıklar
        "1AO": "intangible_assets",             # Maddi olmayan varlıklar
        "1AR": "tax_assets",                    # Vergi varlıkları
        
        # BALANCE SHEET - LIABILITIES & EQUITY
        "2Z": "total_liabilities_equity",       # Toplam kaynaklar (kontrol)
        "2A": "deposits",                       # Mevduat
        "2C": "borrowed_funds",                 # Alınan krediler
        "2D": "money_market_funds",             # Para piyasası borçları
        "2E": "securities_issued",              # İhraç edilen menkul değerler
        "2L": "provisions",                     # Karşılıklar
        "2M": "tax_liabilities",                # Vergi yükümlülükleri
        "2NBA": "subordinated_debt",            # Sermaye benzeri krediler
        "2O": "shareholders_equity",            # Özkaynaklar
        "2OV": "period_net_income",             # Dönem net karı (bilanço)
        "2OVA": "minority_interests",           # Azınlık payları
        
        # INCOME STATEMENT
        "3A": "interest_income",                # Faiz gelirleri
        "3B": "interest_expense",               # Faiz giderleri
        "3C": "net_interest_income",            # Net faiz geliri
        "3CA": "net_commission_income",         # Net ücret ve komisyon geliri
        "3CAA": "commission_income",            # Alınan komisyonlar
        "3CAD": "commission_expense",           # Verilen komisyonlar
        "3CB": "dividend_income",               # Temettü gelirleri
        "3CC": "trading_income",                # Ticari kâr/zarar
        "3CD": "other_operating_income",        # Diğer faaliyet gelirleri
        "3CE": "total_operating_income",        # Toplam faaliyet geliri
        "3CF": "provision_expense",             # Kredi ve diğer karşılıklar
        "3CG": "operating_expenses",            # Faaliyet giderleri
        "3CH": "operating_profit",              # Net faaliyet kârı (PPOP benzeri)
        "3CL": "profit_before_tax",             # Vergi öncesi kâr
        "3CM": "tax_expense",                   # Vergi karşılığı
        "3CN": "continuing_operations_income",  # Sürdürülen faaliyetler net kârı
        "3Z": "total_net_income",               # Toplam net kâr (konsolide)
        "3ZA": "net_income",                    # Ana ortaklık net kârı (MAIN!)
        "3ZB": "minority_net_income",           # Azınlık net kârı

        # INSURANCE-SPECIFIC ITEMS (under UFRS_K/S because KAP uses financial institutions template)
        "3AA": "net_premium_income",            # Kazanılmış Primler (Reasürör Payı Düşülmüş Olarak)
        "3BA": "net_claims_incurred",           # Gerçekleşen Hasarlar (Reasürör Payı Düşülmüş Olarak)
        "3BAA": "claims_paid",                  # Ödenen Hasarlar (Reasürör Payı Düşülmüş Olarak)
        "3BAB": "outstanding_claims_change",    # Muallak Hasarlar Karşılığı Değişimi
        "3BD": "operating_expenses",            # Faaliyet Giderleri (Sigorta)
        "3NJD": "net_income",                   # Dönem Net Kar veya Zararı
    }
    
    # XI_29 (Industrial) mappings - generalized structure
    XI_29_MAPPINGS = {
        # BALANCE SHEET - ASSETS (1X codes)
        "1BL": "total_assets",           # TOPLAM VARLIKLAR
        "1A": "current_assets",          # Dönen Varlıklar
        "1AA": "cash_and_equivalents",   # Nakit ve Nakit Benzerleri
        "1AB": "financial_investments_current",  # Finansal Yatırımlar
        "1AC": "accounts_receivable",    # Ticari Alacaklar
        "1AD": "other_receivables",      # Finans Sektörü Faaliyetlerinden Alacaklar
        "1AF": "inventories",            # Stoklar
        "1AK": "non_current_assets",     # Duran Varlıklar
        "1BG": "property_plant_equipment",  # Maddi Duran Varlıklar
        "1BH": "intangible_assets",      # Maddi Olmayan Duran Varlıklar
        "1BGA": "goodwill",              # Şerefiye
        
        # BALANCE SHEET - LIABILITIES (2X codes)
        "2ODB": "total_liabilities_equity",  # TOPLAM KAYNAKLAR
        "2A": "current_liabilities",     # Kısa Vadeli Yükümlülükler
        "2AA": "short_term_borrowings",  # Finansal Borçlar (Kısa Vadeli)
        "2AAGAA": "accounts_payable",    # Ticari Borçlar
        "2B": "non_current_liabilities", # Uzun Vadeli Yükümlülükler
        "2BA": "long_term_borrowings",   # Finansal Borçlar (Uzun Vadeli)
        "2N": "shareholders_equity",     # Özkaynaklar
        "2O": "shareholders_equity",     # Ana Ortaklığa Ait Özkaynaklar (also shareholders_equity)
        "2OA": "paid_in_capital",        # Ödenmiş Sermaye
        "2OCF": "retained_earnings",     # Dönem Net Kar/Zararı
        "2OCE": "retained_earnings",     # Geçmiş Yıllar Kar/Zararları
        
        # INCOME STATEMENT (3X codes)
        "3C": "revenue",                 # Satış Gelirleri
        "3CA": "cost_of_goods_sold",     # Satışların Maliyeti
        "3CAB": "gross_profit",          # Ticari Faaliyetlerden Brüt Kar
        "3D": "gross_profit",            # BRÜT KAR (ZARAR)
        "3DF": "operating_income",       # FAALİYET KARI (ZARARI)
        "3H": "operating_income",        # Net Faaliyet Kar/Zararı
        "3HB": "financial_income",       # Finansal Gelirler
        "3HC": "financial_expense",      # Finansal Giderler
        "3I": "profit_before_tax",       # Vergi Öncesi Kar
        "3J": "net_income_continuing",   # Sürdürülen Faaliyetler Dönem Karı
        "3L": "net_income",              # DÖNEM KARI (ZARARI)
        "3Z": "net_income",              # Ana Ortaklık Payları (net income to shareholders)
        
        # CASH FLOW STATEMENT (4X codes)
        "4C": "operating_cash_flow",     # İşletme Faaliyetlerinden Nakit
        "4CAB": "depreciation_amortization",  # Amortisman & İtfa Payları
        "4CB": "free_cash_flow",         # Serbest Nakit Akım
    }
    
    # Mapping configurations by financial group
    MAPPINGS = {
        "UFRS_K": UFRS_K_MAPPINGS,
        "UFRS_F": UFRS_K_MAPPINGS,  # Finance companies similar to banks
        "UFRS_S": UFRS_K_MAPPINGS,  # Insurance companies similar structure
        "XI_29": XI_29_MAPPINGS,
    }
    
    def __init__(self, db: Session):
        self.db = db
        self._cache: Dict[str, Dict[str, str]] = {}
    
    def get_semantic_name(self, item_code: str, financial_group: str) -> Optional[str]:
        """
        Get semantic name for an item code
        
        Args:
            item_code: İş Yatırım item code (e.g., '1Z', '3ZA')
            financial_group: Financial group (e.g., 'UFRS_K', 'XI_29')
            
        Returns:
            Semantic name (e.g., 'total_assets', 'net_income') or None
        """
        # Check cache first
        cache_key = f"{financial_group}:{item_code}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Check database mapping
        mapping = self.db.query(ItemCodeMapping).filter(
            and_(
                ItemCodeMapping.financial_group == financial_group,
                ItemCodeMapping.item_code == item_code
            )
        ).first()
        
        if mapping:
            semantic_name = mapping.semantic_name
            self._cache[cache_key] = semantic_name
            return semantic_name
        
        # Fallback to hardcoded mappings
        group_mappings = self.MAPPINGS.get(financial_group, {})
        semantic_name = group_mappings.get(item_code)
        
        if semantic_name:
            # Cache the result
            self._cache[cache_key] = semantic_name
            
            # Optionally save to database for future use
            try:
                self._save_mapping(item_code, semantic_name, financial_group)
            except Exception as e:
                logger.warning(f"Failed to save mapping {item_code}->{semantic_name}: {e}")
        
        return semantic_name
    
    def _save_mapping(
        self, 
        item_code: str, 
        semantic_name: str, 
        financial_group: str,
        description: Optional[str] = None
    ):
        """Save a mapping to database"""
        try:
            # Check if this item_code already exists
            existing = self.db.query(ItemCodeMapping).filter(
                and_(
                    ItemCodeMapping.financial_group == financial_group,
                    ItemCodeMapping.item_code == item_code
                )
            ).first()
            
            if existing:
                existing.semantic_name = semantic_name
                if description:
                    existing.description_tr = description
            else:
                # Check if semantic_name already exists for this financial_group
                # If so, skip to avoid duplicate key error
                existing_semantic = self.db.query(ItemCodeMapping).filter(
                    and_(
                        ItemCodeMapping.financial_group == financial_group,
                        ItemCodeMapping.semantic_name == semantic_name
                    )
                ).first()
                
                if existing_semantic:
                    # Skip - don't create duplicate semantic names
                    logger.debug(f"Semantic name '{semantic_name}' already exists for {financial_group}, skipping {item_code}")
                    return
                
                mapping = ItemCodeMapping(
                    financial_group=financial_group,
                    item_code=item_code,
                    semantic_name=semantic_name,
                    description_tr=description or f"Auto-mapped: {item_code}",
                    statement_type=self._classify_statement_type(item_code),
                    category=self._classify_category(item_code, semantic_name),
                    is_primary=True,
                    priority=1000
                )
                self.db.add(mapping)
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.warning(f"Failed to save mapping {item_code}->{semantic_name}: {e}")
    
    def _classify_statement_type(self, item_code: str) -> str:
        """Classify statement type based on item code"""
        if not item_code:
            return "unknown"
        
        first_char = item_code[0]
        if first_char in ["1", "2"]:
            return "balance_sheet"
        elif first_char == "3":
            return "income_statement"
        elif first_char == "4":
            return "cash_flow"
        else:
            return "unknown"
    
    def _classify_category(self, item_code: str, semantic_name: str) -> str:
        """Classify account category"""
        if not item_code:
            return "unknown"
        
        first_char = item_code[0]
        
        if first_char == "1":
            return "asset"
        elif first_char == "2":
            if "equity" in semantic_name.lower() or item_code.startswith("2O"):
                return "equity"
            else:
                return "liability"
        elif first_char == "3":
            if any(word in semantic_name.lower() for word in ["revenue", "income", "profit"]):
                return "revenue"
            else:
                return "expense"
        elif first_char == "4":
            return "cash_flow"
        else:
            return "unknown"
    
    def get_all_mappings(self, financial_group: str) -> Dict[str, str]:
        """Get all mappings for a financial group"""
        # Get from database
        db_mappings = self.db.query(ItemCodeMapping).filter(
            ItemCodeMapping.financial_group == financial_group
        ).all()
        
        mappings = {}
        for mapping in db_mappings:
            mappings[mapping.item_code] = mapping.semantic_name
        
        # Merge with hardcoded mappings
        hardcoded = self.MAPPINGS.get(financial_group, {})
        mappings.update(hardcoded)
        
        return mappings
    
    def bulk_save_mappings(
        self, 
        financial_group: str, 
        mappings: Dict[str, str],
        overwrite: bool = False
    ):
        """Save multiple mappings at once"""
        for item_code, semantic_name in mappings.items():
            existing = self.db.query(ItemCodeMapping).filter(
                and_(
                    ItemCodeMapping.financial_group == financial_group,
                    ItemCodeMapping.item_code == item_code
                )
            ).first()
            
            if existing and not overwrite:
                continue
            
            if existing:
                existing.semantic_name = semantic_name
            else:
                mapping = ItemCodeMapping(
                    financial_group=financial_group,
                    item_code=item_code,
                    semantic_name=semantic_name,
                    statement_type=self._classify_statement_type(item_code),
                    category=self._classify_category(item_code, semantic_name),
                    is_primary=True,
                    priority=1000
                )
                self.db.add(mapping)
        
        self.db.commit()
        logger.info(f"✅ Saved {len(mappings)} mappings for {financial_group}")
    
    def validate_mapping_coverage(self, ticker: str, financial_group: str) -> Dict[str, Any]:
        """Validate mapping coverage for a company"""
        from models.financial import FinancialStatementRaw
        
        # Get all item codes for this company
        item_codes = self.db.query(FinancialStatementRaw.item_code).filter(
            and_(
                FinancialStatementRaw.ticker == ticker,
                FinancialStatementRaw.financial_group == financial_group
            )
        ).distinct().all()
        
        item_codes = [code[0] for code in item_codes]
        
        # Check mapping coverage
        mapped = 0
        unmapped = []
        
        for item_code in item_codes:
            semantic_name = self.get_semantic_name(item_code, financial_group)
            if semantic_name:
                mapped += 1
            else:
                unmapped.append(item_code)
        
        total = len(item_codes)
        coverage_pct = (mapped / total * 100) if total > 0 else 0
        
        return {
            "ticker": ticker,
            "financial_group": financial_group,
            "total_codes": total,
            "mapped": mapped,
            "unmapped": len(unmapped),
            "coverage_pct": round(coverage_pct, 1),
            "unmapped_codes": unmapped[:10],  # First 10 unmapped codes
            "status": "good" if coverage_pct >= 80 else "needs_attention" if coverage_pct >= 60 else "poor"
        }