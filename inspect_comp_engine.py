"""
COMP Engine Inspector - Data Quality Analysis
"""
from core.database import SessionLocal
from models.financial import FinancialStatementRaw, CompanyRatio
from models.benchmark import SectorBenchmark
from models.company import Company
from sqlalchemy import text

with SessionLocal() as db:
    # Company stats
    total_companies = db.query(Company).count()
    active_companies = db.query(Company).filter(Company.is_active == True).count()
    
    # Financial statements stats
    total_statements = db.query(FinancialStatementRaw).count()
    
    # Statements by financial group
    groups = db.execute(text('''
        SELECT financial_group, COUNT(*) as cnt, COUNT(DISTINCT ticker) as companies
        FROM financial_statements_raw
        GROUP BY financial_group
        ORDER BY cnt DESC
    ''')).fetchall()
    
    # Statements by sector
    sectors = db.execute(text('''
        SELECT c.sector_main, COUNT(*) as cnt, COUNT(DISTINCT fsr.ticker) as companies
        FROM financial_statements_raw fsr
        JOIN companies c ON fsr.ticker = c.ticker
        GROUP BY c.sector_main
        ORDER BY cnt DESC
    ''')).fetchall()
    
    # Ratio stats
    total_ratios = db.query(CompanyRatio).count()
    
    # Ratios by category
    ratio_categories = db.execute(text('''
        SELECT 
            CASE 
                WHEN ratio_code IN ('current_ratio', 'acid_test_ratio') THEN 'Liquidity'
                WHEN ratio_code IN ('debt_to_equity', 'debt_ratio', 'net_debt_to_equity') THEN 'Leverage'
                WHEN ratio_code IN ('gross_margin', 'operating_margin', 'net_margin', 'ebitda_margin', 'roe', 'roa') THEN 'Profitability'
                WHEN ratio_code IN ('pe_ratio', 'pb_ratio', 'ev_ebitda') THEN 'Valuation'
                WHEN ratio_code IN ('asset_turnover', 'inventory_turnover', 'receivables_turnover') THEN 'Efficiency'
                WHEN ratio_code IN ('net_interest_margin', 'loan_to_deposit', 'npl_ratio', 'capital_adequacy', 'cost_income_ratio') THEN 'Banking'
                ELSE 'Other'
            END as category,
            COUNT(*) as cnt
        FROM company_ratios
        GROUP BY category
        ORDER BY cnt DESC
    ''')).fetchall()
    
    # Benchmark stats
    total_benchmarks = db.query(SectorBenchmark).count()
    
    # Benchmarks by reliability
    reliability = db.execute(text('''
        SELECT reliability, COUNT(*) as cnt
        FROM sector_benchmarks
        GROUP BY reliability
        ORDER BY cnt DESC
    ''')).fetchall()
    
    # Period coverage
    periods = db.execute(text('''
        SELECT period_key, COUNT(DISTINCT ticker) as companies, COUNT(*) as rows
        FROM financial_statements_raw
        GROUP BY period_key
        ORDER BY period_key DESC
        LIMIT 10
    ''')).fetchall()
    
    # Unique ratio codes
    unique_ratios = db.execute(text('''
        SELECT ratio_code, COUNT(*) as cnt
        FROM company_ratios
        GROUP BY ratio_code
        ORDER BY cnt DESC
    ''')).fetchall()
    
    # Sample benchmarks
    sample_benchmarks = db.execute(text('''
        SELECT sector_main, ratio_code, period_key, 
               ROUND(median_ew::numeric, 4) as median,
               ROUND(p25::numeric, 4) as p25,
               ROUND(p75::numeric, 4) as p75,
               n_peers, reliability
        FROM sector_benchmarks
        ORDER BY sector_main, ratio_code
        LIMIT 20
    ''')).fetchall()
    
    print('=' * 70)
    print('COMP ENGINE DATA QUALITY REPORT')
    print('=' * 70)
    print()
    print('COMPANIES:')
    print(f'  Total: {total_companies}')
    print(f'  Active: {active_companies}')
    print()
    print('FINANCIAL STATEMENTS:')
    print(f'  Total rows: {total_statements:,}')
    print()
    print('By Financial Group:')
    for g in groups:
        print(f'  {g[0]}: {g[1]:,} rows, {g[2]} companies')
    print()
    print('By Sector:')
    for s in sectors:
        print(f'  {s[0]}: {s[1]:,} rows, {s[2]} companies')
    print()
    print('PERIOD COVERAGE (Latest 10):')
    for p in periods:
        print(f'  {p[0]}: {p[1]} companies, {p[2]:,} rows')
    print()
    print('RATIOS:')
    print(f'  Total: {total_ratios:,}')
    print()
    print('By Category:')
    for rc in ratio_categories:
        print(f'  {rc[0]}: {rc[1]:,}')
    print()
    print('UNIQUE RATIO CODES:')
    for u in unique_ratios:
        print(f'  {u[0]}: {u[1]:,}')
    print()
    print('BENCHMARKS:')
    print(f'  Total: {total_benchmarks:,}')
    print()
    print('By Reliability:')
    for r in reliability:
        print(f'  {r[0]}: {r[1]:,}')
    print()
    print('SAMPLE BENCHMARKS:')
    print('-' * 100)
    for b in sample_benchmarks:
        print(f'{b[0]:<25} {b[1]:<20} {b[2]:<10} median={b[3]} p25={b[4]} p75={b[5]} n={b[6]} {b[7]}')
