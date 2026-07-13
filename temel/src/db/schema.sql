-- Companies
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    name_en TEXT,
    sector_raw TEXT,
    sector_main TEXT NOT NULL,
    industry TEXT,
    financial_group TEXT NOT NULL DEFAULT 'XI_29',
    market_cap INTEGER,
    shares_outstanding INTEGER,
    free_float_pct REAL,
    city TEXT,
    website TEXT,
    about TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_companies_sector ON companies(sector_main);
CREATE INDEX IF NOT EXISTS idx_companies_active ON companies(is_active);
CREATE INDEX IF NOT EXISTS idx_companies_ticker ON companies(ticker);

-- Financial Statements (raw from İş Yatırım)
CREATE TABLE IF NOT EXISTS financial_statements_raw (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    period_key TEXT NOT NULL,
    year INTEGER NOT NULL,
    period INTEGER NOT NULL,
    financial_group TEXT NOT NULL,
    item_code TEXT NOT NULL,
    item_desc_tr TEXT,
    item_desc_en TEXT,
    value_try REAL,
    currency TEXT DEFAULT 'TRY',
    fetched_at TEXT NOT NULL,
    UNIQUE(ticker, period_key, item_code)
);

CREATE INDEX IF NOT EXISTS idx_fsr_ticker ON financial_statements_raw(ticker);
CREATE INDEX IF NOT EXISTS idx_fsr_period ON financial_statements_raw(period_key);
CREATE INDEX IF NOT EXISTS idx_fsr_ticker_period ON financial_statements_raw(ticker, period_key);
CREATE INDEX IF NOT EXISTS idx_fsr_item_code ON financial_statements_raw(item_code);

-- Calculated Ratios
CREATE TABLE IF NOT EXISTS company_ratios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    period_key TEXT NOT NULL,
    ratio_code TEXT NOT NULL,
    ratio_value REAL,
    is_ttm INTEGER DEFAULT 0,
    calculation_method TEXT,
    data_quality_score REAL,
    computed_at TEXT NOT NULL,
    UNIQUE(ticker, period_key, ratio_code)
);

CREATE INDEX IF NOT EXISTS idx_cr_ticker ON company_ratios(ticker);
CREATE INDEX IF NOT EXISTS idx_cr_period ON company_ratios(period_key);
CREATE INDEX IF NOT EXISTS idx_cr_ticker_code ON company_ratios(ticker, ratio_code);
CREATE INDEX IF NOT EXISTS idx_cr_period_code ON company_ratios(period_key, ratio_code);

-- Company Market Metrics
CREATE TABLE IF NOT EXISTS company_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE NOT NULL,
    last_price REAL,
    market_cap INTEGER,
    shares_outstanding INTEGER,
    free_float_pct REAL,
    volume_1d INTEGER,
    volume_avg_30d INTEGER,
    pe_ratio REAL,
    pb_ratio REAL,
    price_updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_cm_ticker ON company_metrics(ticker);

-- Item Code Mappings (İş Yatırım codes -> semantic names)
CREATE TABLE IF NOT EXISTS item_code_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    financial_group TEXT NOT NULL,
    item_code TEXT NOT NULL,
    semantic_name TEXT NOT NULL,
    description_tr TEXT,
    description_en TEXT,
    statement_type TEXT NOT NULL,
    category TEXT NOT NULL,
    is_primary INTEGER DEFAULT 1,
    priority INTEGER DEFAULT 1000,
    UNIQUE(financial_group, item_code),
    UNIQUE(financial_group, semantic_name)
);

CREATE INDEX IF NOT EXISTS idx_icm_group ON item_code_mappings(financial_group);
CREATE INDEX IF NOT EXISTS idx_icm_semantic ON item_code_mappings(semantic_name);

-- Company Financial Summary (ShortTable data — 3 key items per period)
CREATE TABLE IF NOT EXISTS company_financial_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    period_key TEXT NOT NULL,
    equity REAL,
    paid_capital REAL,
    net_income REAL,
    fetched_at TEXT NOT NULL,
    UNIQUE(ticker, period_key)
);

CREATE INDEX IF NOT EXISTS idx_cfs_ticker ON company_financial_summary(ticker);
CREATE INDEX IF NOT EXISTS idx_cfs_period ON company_financial_summary(period_key);

-- Fetch Logs (audit trail)
CREATE TABLE IF NOT EXISTS fetch_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    period_key TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    http_status INTEGER,
    response_size INTEGER,
    processing_time_ms INTEGER,
    checksum_md5 TEXT,
    is_new_data INTEGER DEFAULT 0,
    error_message TEXT
);

CREATE INDEX IF NOT EXISTS idx_fl_ticker ON fetch_logs(ticker);
CREATE INDEX IF NOT EXISTS idx_fl_period ON fetch_logs(period_key);
CREATE INDEX IF NOT EXISTS idx_fl_ticker_period ON fetch_logs(ticker, period_key);

-- İş Yatırım Reference Ratios (bootstrapped from Excel exports)
CREATE TABLE IF NOT EXISTS isyatirim_ratios (
    ticker TEXT PRIMARY KEY,
    sector TEXT,
    last_price REAL,
    market_cap_tl REAL,
    market_cap_usd REAL,
    free_float_pct REAL,
    capital_mn_tl REAL,
    pe_ratio REAL,
    ev_ebitda REAL,
    ev_sales REAL,
    pb_ratio REAL,
    forward_pe REAL,
    forward_ev_ebitda REAL,
    forward_pb REAL,
    last_period TEXT,
    data_date TEXT,
    fetched_at TEXT DEFAULT (datetime('now'))
);

-- Company Sector Profiles (characteristic-based classification)
CREATE TABLE IF NOT EXISTS company_sector_profiles (
    ticker TEXT PRIMARY KEY,
    sector_name TEXT,
    sector_group TEXT,
    has_loans INTEGER DEFAULT 0,
    has_insurance INTEGER DEFAULT 0,
    has_inventory INTEGER DEFAULT 0,
    has_receivables INTEGER DEFAULT 0,
    is_financial INTEGER DEFAULT 0,
    is_holding INTEGER DEFAULT 0,
    is_reit INTEGER DEFAULT 0
);

-- Sector Benchmarks (medians, percentiles per sector/group/market)
CREATE TABLE IF NOT EXISTS sector_benchmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_name TEXT NOT NULL,
    benchmark_type TEXT NOT NULL,
    ratio_code TEXT NOT NULL,
    period_key TEXT NOT NULL,
    median_ew REAL,
    median_mc REAL,
    p25 REAL,
    p75 REAL,
    n_peers INTEGER,
    reliability TEXT,
    computed_at TEXT NOT NULL,
    UNIQUE(sector_name, benchmark_type, ratio_code, period_key)
);

CREATE INDEX IF NOT EXISTS idx_sb_sector ON sector_benchmarks(sector_name, benchmark_type);
CREATE INDEX IF NOT EXISTS idx_sb_period ON sector_benchmarks(period_key);

-- Company Scores (composite + pillar breakdown)
CREATE TABLE IF NOT EXISTS company_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    period_key TEXT NOT NULL DEFAULT 'TTM',
    composite_score REAL,
    reliability TEXT,
    pillar_finansal_saglik REAL,
    pillar_karlilik_buyume REAL,
    pillar_degerleme REAL,
    benchmark_source TEXT,
    n_peers INTEGER,
    data_completeness REAL,
    upper_sector_name TEXT,
    upper_benchmark_type TEXT,
    absolute_score REAL,
    absolute_label TEXT,
    score_version TEXT DEFAULT 'v1',
    computed_at TEXT NOT NULL,
    UNIQUE(ticker, period_key, score_version)
);

CREATE INDEX IF NOT EXISTS idx_cs_ticker ON company_scores(ticker);
CREATE INDEX IF NOT EXISTS idx_cs_period ON company_scores(period_key);

-- Company Score Details (ratio-level breakdown)
CREATE TABLE IF NOT EXISTS company_score_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score_id INTEGER NOT NULL,
    ratio_code TEXT NOT NULL,
    ratio_value REAL,
    peer_median REAL,
    percentile REAL,
    raw_score REAL,
    final_score REAL,
    higher_is_better INTEGER DEFAULT 1,
    reliability TEXT,
    pillar TEXT,
    FOREIGN KEY (score_id) REFERENCES company_scores(id)
);

CREATE INDEX IF NOT EXISTS idx_csd_score ON company_score_details(score_id);

-- Sector Consolidation Map (54 raw sectors -> 14 consolidated groups)
CREATE TABLE IF NOT EXISTS sector_consolidation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_raw TEXT NOT NULL UNIQUE,
    sector_group TEXT,
    sector_consolidated TEXT,
    is_spor INTEGER DEFAULT 0
);
