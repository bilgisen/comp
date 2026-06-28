"""
Update Item Code Mappings in Database
Clear old mappings and insert new correct ones
"""
from core.database import SessionLocal
from models.financial import ItemCodeMapping
from services.item_code_mapper import ItemCodeMapper
from sqlalchemy import text

# XI_29 mappings (Industrial companies)
XI_29_MAPPINGS = {
    # BALANCE SHEET - ASSETS
    "1BL": ("total_assets", "TOPLAM VARLIKLAR", "balance_sheet", "asset"),
    "1A": ("current_assets", "Dönen Varlıklar", "balance_sheet", "asset"),
    "1AA": ("cash_and_equivalents", "Nakit ve Nakit Benzerleri", "balance_sheet", "asset"),
    "1AB": ("financial_investments_current", "Finansal Yatırımlar (Dönen)", "balance_sheet", "asset"),
    "1AC": ("accounts_receivable", "Ticari Alacaklar", "balance_sheet", "asset"),
    "1AD": ("other_receivables", "Finans Sektörü Faaliyetlerinden Alacaklar", "balance_sheet", "asset"),
    "1AF": ("inventories", "Stoklar", "balance_sheet", "asset"),
    "1AH": ("other_current_assets", "Diğer Dönen Varlıklar", "balance_sheet", "asset"),
    "1AK": ("non_current_assets", "Duran Varlıklar", "balance_sheet", "asset"),
    "1BG": ("property_plant_equipment", "Maddi Duran Varlıklar", "balance_sheet", "asset"),
    "1BGA": ("goodwill", "Şerefiye", "balance_sheet", "asset"),
    "1BH": ("intangible_assets", "Maddi Olmayan Duran Varlıklar", "balance_sheet", "asset"),
    
    # BALANCE SHEET - LIABILITIES
    "2ODB": ("total_liabilities_equity", "TOPLAM KAYNAKLAR", "balance_sheet", "liability"),
    "2A": ("current_liabilities", "Kısa Vadeli Yükümlülükler", "balance_sheet", "liability"),
    "2AA": ("short_term_borrowings", "Finansal Borçlar (Kısa Vadeli)", "balance_sheet", "liability"),
    "2AAGAA": ("accounts_payable", "Ticari Borçlar", "balance_sheet", "liability"),
    "2B": ("non_current_liabilities", "Uzun Vadeli Yükümlülükler", "balance_sheet", "liability"),
    "2BA": ("long_term_borrowings", "Finansal Borçlar (Uzun Vadeli)", "balance_sheet", "liability"),
    "2N": ("shareholders_equity_total", "Özkaynaklar (Toplam)", "balance_sheet", "equity"),
    "2O": ("shareholders_equity", "Ana Ortaklığa Ait Özkaynaklar", "balance_sheet", "equity"),
    "2OA": ("paid_in_capital", "Ödenmiş Sermaye", "balance_sheet", "equity"),
    "2OCF": ("period_net_income", "Dönem Net Kar/Zararı", "balance_sheet", "equity"),
    "2OCE": ("retained_earnings", "Geçmiş Yıllar Kar/Zararları", "balance_sheet", "equity"),
    
    # INCOME STATEMENT
    "3C": ("revenue", "Satış Gelirleri", "income_statement", "revenue"),
    "3CA": ("cost_of_goods_sold", "Satışların Maliyeti", "income_statement", "expense"),
    "3CAB": ("gross_profit_trade", "Ticari Faaliyetlerden Brüt Kar", "income_statement", "revenue"),
    "3D": ("gross_profit", "BRÜT KAR (ZARAR)", "income_statement", "revenue"),
    "3DA": ("selling_expenses", "Pazarlama, Satış ve Dağıtım Giderleri", "income_statement", "expense"),
    "3DB": ("administrative_expenses", "Genel Yönetim Giderleri", "income_statement", "expense"),
    "3DC": ("research_development", "Araştırma ve Geliştirme Giderleri", "income_statement", "expense"),
    "3DF": ("operating_income", "FAALİYET KARI (ZARARI)", "income_statement", "revenue"),
    "3H": ("operating_income_alt", "Net Faaliyet Kar/Zararı", "income_statement", "revenue"),
    "3HB": ("financial_income", "Finansal Gelirler", "income_statement", "revenue"),
    "3HC": ("financial_expense", "Finansal Giderler", "income_statement", "expense"),
    "3I": ("profit_before_tax", "Vergi Öncesi Kar", "income_statement", "revenue"),
    "3J": ("net_income_continuing", "Sürdürülen Faaliyetler Dönem Karı", "income_statement", "revenue"),
    "3L": ("net_income_total", "DÖNEM KARI (ZARARI)", "income_statement", "revenue"),
    "3Z": ("net_income", "Ana Ortaklık Payları", "income_statement", "revenue"),
    
    # CASH FLOW STATEMENT
    "4C": ("operating_cash_flow", "İşletme Faaliyetlerinden Nakit", "cash_flow", "cash_flow"),
    "4CAB": ("depreciation_amortization", "Amortisman & İtfa Payları", "cash_flow", "cash_flow"),
    "4CB": ("free_cash_flow", "Serbest Nakit Akım", "cash_flow", "cash_flow"),
}

# UFRS_K mappings (Banking)
UFRS_K_MAPPINGS = {
    # BALANCE SHEET - ASSETS
    "1Z": ("total_assets", "TOPLAM VARLIKLAR", "balance_sheet", "asset"),
    "1A": ("cash_and_cb", "Nakit + Merkez Bankası", "balance_sheet", "asset"),
    "1AC": ("banks_correspondent", "Muhabir bankalar", "balance_sheet", "asset"),
    "1AF": ("gross_loans", "Brüt krediler", "balance_sheet", "asset"),
    "1AFD": ("non_performing_loans", "Takipteki krediler", "balance_sheet", "asset"),
    "1AN": ("tangible_assets", "Maddi duran varlıklar", "balance_sheet", "asset"),
    "1AO": ("intangible_assets", "Maddi olmayan varlıklar", "balance_sheet", "asset"),
    
    # BALANCE SHEET - LIABILITIES & EQUITY
    "2Z": ("total_liabilities_equity", "Toplam kaynaklar", "balance_sheet", "liability"),
    "2A": ("deposits", "Mevduat", "balance_sheet", "liability"),
    "2C": ("borrowed_funds", "Alınan krediler", "balance_sheet", "liability"),
    "2O": ("shareholders_equity", "Özkaynaklar", "balance_sheet", "equity"),
    "2OV": ("period_net_income", "Dönem net karı", "balance_sheet", "equity"),
    
    # INCOME STATEMENT
    "3A": ("interest_income", "Faiz gelirleri", "income_statement", "revenue"),
    "3B": ("interest_expense", "Faiz giderleri", "income_statement", "expense"),
    "3C": ("net_interest_income", "Net faiz geliri", "income_statement", "revenue"),
    "3CA": ("net_commission_income", "Net ücret ve komisyon geliri", "income_statement", "revenue"),
    "3CE": ("total_operating_income", "Toplam faaliyet geliri", "income_statement", "revenue"),
    "3CG": ("operating_expenses", "Faaliyet giderleri", "income_statement", "expense"),
    "3CH": ("operating_profit", "Net faaliyet kârı", "income_statement", "revenue"),
    "3CL": ("profit_before_tax", "Vergi öncesi kâr", "income_statement", "revenue"),
    "3Z": ("total_net_income", "Toplam net kâr", "income_statement", "revenue"),
    "3ZA": ("net_income", "Ana ortaklık net kârı", "income_statement", "revenue"),
}


def update_mappings():
    """Update all mappings in database"""
    with SessionLocal() as db:
        # Clear existing mappings
        db.execute(text("DELETE FROM item_code_mappings"))
        db.commit()
        print("Cleared existing mappings")
        
        # Insert XI_29 mappings
        for item_code, (semantic_name, desc_tr, stmt_type, category) in XI_29_MAPPINGS.items():
            mapping = ItemCodeMapping(
                financial_group="XI_29",
                item_code=item_code,
                semantic_name=semantic_name,
                description_tr=desc_tr,
                statement_type=stmt_type,
                category=category,
                is_primary=True,
                priority=100
            )
            db.add(mapping)
        
        print(f"Added {len(XI_29_MAPPINGS)} XI_29 mappings")
        
        # Insert UFRS_K mappings
        for item_code, (semantic_name, desc_tr, stmt_type, category) in UFRS_K_MAPPINGS.items():
            mapping = ItemCodeMapping(
                financial_group="UFRS_K",
                item_code=item_code,
                semantic_name=semantic_name,
                description_tr=desc_tr,
                statement_type=stmt_type,
                category=category,
                is_primary=True,
                priority=100
            )
            db.add(mapping)
        
        print(f"Added {len(UFRS_K_MAPPINGS)} UFRS_K mappings")
        
        # Also add for UFRS_F and UFRS_S (same as UFRS_K)
        for fg in ["UFRS_F", "UFRS_S"]:
            for item_code, (semantic_name, desc_tr, stmt_type, category) in UFRS_K_MAPPINGS.items():
                mapping = ItemCodeMapping(
                    financial_group=fg,
                    item_code=item_code,
                    semantic_name=semantic_name,
                    description_tr=desc_tr,
                    statement_type=stmt_type,
                    category=category,
                    is_primary=True,
                    priority=100
                )
                db.add(mapping)
        
        print(f"Added mappings for UFRS_F and UFRS_S")
        
        db.commit()
        print("All mappings saved successfully!")
        
        # Verify
        count = db.query(ItemCodeMapping).count()
        print(f"Total mappings in database: {count}")


if __name__ == "__main__":
    update_mappings()
