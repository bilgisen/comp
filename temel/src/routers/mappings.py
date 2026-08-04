FINANCIAL_GROUP_LABELS = {
    "XI_29": "TMS/TFRS",
    "UFRS_K": "UFRS Konsolide",
    "UFRS_S": "UFRS Sigorta",
    "UFRS_F": "UFRS Finansal Kiralama",
}

STATEMENT_TYPE_LABELS = {
    "balance_sheet": "Bilanço",
    "income_statement": "Gelir Tablosu",
    "cash_flow": "Nakit Akış Tablosu",
}

RATIO_NAMES = {
    "current_ratio": "Cari Oran",
    "acid_test_ratio": "Asit Test Oranı",
    "debt_to_equity": "Borç/Özkaynak",
    "debt_ratio": "Borçlanma Oranı",
    "gross_margin": "Brüt Kâr Marjı",
    "net_margin": "Net Kâr Marjı",
    "roe": "Özkaynak Kârlılığı (ROE)",
    "roa": "Aktif Kârlılığı (ROA)",
    "pe_ratio": "F/K Oranı",
    "pb_ratio": "PD/DD Oranı",
    "ev_ebitda": "FD/FAVÖK",
    "ev_sales": "FD/Satışlar",
    "eps": "Hisse Başına Kâr",
    "book_per_share": "Defter Değeri",
    "profit_growth": "Kâr Büyümesi",
    "cash_ratio": "Nakit Oranı",
    "inventory_turnover": "Stok Devir Hızı",
    "interest_coverage": "Faiz Karşılama Oranı",
    "net_debt_to_equity": "Net Borç/Özkaynak",
    "asset_turnover": "Aktif Devir Hızı",
    "operating_margin": "Faaliyet Kâr Marjı",
    "ebitda_margin": "FAVÖK Marjı",
    "forward_pe": "İleri F/K",
    "forward_ev_ebitda": "İleri FD/FAVÖK",
    "forward_pb": "İleri PD/DD",
    "pe": "F/K Oranı",
    "pb": "PD/DD Oranı",
    "debt_equity": "Borç/Özkaynak",
}

# v1 (legacy periyodik) -> v2 (TTM worker) ratio code aliases
RATIO_CODE_ALIASES = {
    "pe_ratio": "pe",
    "pb_ratio": "pb",
    "debt_to_equity": "debt_equity",
}


def map_financial_group(code):
    return FINANCIAL_GROUP_LABELS.get(code, code)


def map_statement_type(st):
    return STATEMENT_TYPE_LABELS.get(st, st)


def map_ratio_name(code):
    return RATIO_NAMES.get(code, code)
