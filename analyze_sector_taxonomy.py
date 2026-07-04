"""
Analyze Sector Taxonomy and Identify Heterogeneous Sectors
Identifies which sectors have diverse sub-sectors that need separate benchmarking
"""

from sqlalchemy import create_engine, text
from core.config import settings

sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
engine = create_engine(sync_db_url)

print("🔍 SECTOR TAXONOMY ANALYSIS")
print("=" * 80)

with engine.connect() as conn:
    # Analyze all sectors - group by sector_main and financial_group
    result = conn.execute(text("""
        SELECT 
            sector_main,
            financial_group,
            COUNT(*) as company_count,
            STRING_AGG(ticker, ', ' ORDER BY ticker) as tickers
        FROM companies
        WHERE is_active = TRUE
        GROUP BY sector_main, financial_group
        ORDER BY sector_main, company_count DESC
    """))
    
    sector_data = {}
    for row in result:
        sector = row.sector_main
        if sector not in sector_data:
            sector_data[sector] = []
        sector_data[sector].append({
            'financial_group': row.financial_group,
            'count': row.company_count,
            'tickers': row.tickers
        })
    
    print(f"\n📊 Total Sectors: {len(sector_data)}")
    print("=" * 80)
    
    # Identify heterogeneous sectors (multiple financial_groups with significant counts)
    heterogeneous_sectors = {}
    
    for sector, groups in sector_data.items():
        total_companies = sum(g['count'] for g in groups)
        num_groups = len(groups)
        
        print(f"\n🏢 {sector} ({total_companies} şirket)")
        print("-" * 80)
        
        if num_groups > 1:
            print(f"   ⚠️ HETEROGENEOUS: {num_groups} farklı financial_group")
            heterogeneous_sectors[sector] = groups
        
        for group in groups:
            pct = (group['count'] / total_companies * 100)
            print(f"   • {group['financial_group']}: {group['count']} şirket ({pct:.1f}%)")
            # Show first few tickers
            ticker_list = group['tickers'].split(', ')
            if len(ticker_list) <= 5:
                print(f"     └─ {group['tickers']}")
            else:
                print(f"     └─ {', '.join(ticker_list[:5])}... (+{len(ticker_list)-5} more)")
    
    # Summary of heterogeneous sectors
    print("\n" + "=" * 80)
    print("🎯 HETEROGENEOUS SECTORS REQUIRING SUB-SECTOR FILTERING:")
    print("=" * 80)
    
    for sector, groups in heterogeneous_sectors.items():
        total = sum(g['count'] for g in groups)
        print(f"\n{sector} ({total} şirket):")
        for group in groups:
            print(f"  • {group['financial_group']}: {group['count']} şirket")
    
    # Get sample ratios for each sector to understand which ratios need filtering
    print("\n" + "=" * 80)
    print("📊 SAMPLE RATIOS BY SECTOR:")
    print("=" * 80)
    
    result = conn.execute(text("""
        SELECT 
            c.sector_main,
            cr.ratio_code,
            COUNT(DISTINCT cr.ticker) as company_count
        FROM company_ratios cr
        JOIN companies c ON cr.ticker = c.ticker
        WHERE c.is_active = TRUE
          AND cr.period_key = (SELECT MAX(period_key) FROM company_ratios)
        GROUP BY c.sector_main, cr.ratio_code
        HAVING COUNT(DISTINCT cr.ticker) >= 3
        ORDER BY c.sector_main, company_count DESC
    """))
    
    ratios_by_sector = {}
    for row in result:
        sector = row.sector_main
        if sector not in ratios_by_sector:
            ratios_by_sector[sector] = []
        ratios_by_sector[sector].append({
            'ratio': row.ratio_code,
            'count': row.company_count
        })
    
    for sector in heterogeneous_sectors.keys():
        if sector in ratios_by_sector:
            ratios = ratios_by_sector[sector][:10]  # Top 10 ratios
            print(f"\n{sector}:")
            for r in ratios:
                print(f"  • {r['ratio']}: {r['count']} şirket")

print("\n" + "=" * 80)
print("✅ Analysis complete")
print("=" * 80)
