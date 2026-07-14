"""Check Garanti Bank ratios and sector benchmarks"""
from sqlalchemy import create_engine, text
from core.config import settings

sync_db_url = settings.database_url.replace('postgresql+asyncpg://', 'postgresql://')
engine = create_engine(sync_db_url)

with engine.connect() as conn:
    # Get latest period
    period = conn.execute(text('''
        SELECT MAX(period_key) FROM company_ratios WHERE ticker = 'GARAN'
    ''')).scalar()
    
    print(f'Latest Period: {period}\n')
    
    # Get Garanti's ROA and ROE
    result = conn.execute(text('''
        SELECT 
            ratio_code,
            ratio_value
        FROM company_ratios
        WHERE ticker = 'GARAN'
          AND period_key = :period
          AND ratio_code IN ('roa', 'roe')
    '''), {'period': period})
    
    garan_ratios = {row.ratio_code: float(row.ratio_value) for row in result}
    
    print(f'Garanti Bankası ({period}):')
    for code, val in garan_ratios.items():
        print(f'  {code.upper()}: {val:.6f} ({val*100:.2f}%)')
    print()
    
    # Get sector median (Bankacılık & Finans)
    result2 = conn.execute(text('''
        SELECT 
            ratio_code,
            median_ew,
            p25,
            p75,
            n_peers
        FROM sector_benchmarks
        WHERE sector_main = 'Bankacılık & Finans'
          AND ratio_code IN ('roa', 'roe')
          AND period_key = :period
    '''), {'period': period})
    
    print(f'Sektör Benchmarkları (Bankacılık & Finans, {period}):')
    benchmarks = {}
    for row in result2:
        med = float(row.median_ew) if row.median_ew else 0
        p25_val = float(row.p25) if row.p25 else 0
        p75_val = float(row.p75) if row.p75 else 0
        print(f'  {row.ratio_code.upper()}: median={med:.6f} ({med*100:.2f}%), P25={p25_val:.6f}, P75={p75_val:.6f}, n_peers={row.n_peers}')
        benchmarks[row.ratio_code] = med
    
    print('\n--- Manuel Hesaplama ---')
    
    for ratio_code in ['roa', 'roe']:
        if ratio_code in benchmarks and ratio_code in garan_ratios:
            val = garan_ratios[ratio_code]
            med = benchmarks[ratio_code]
            
            if med == 0:
                print(f'\n⚠️  {ratio_code.upper()} median SIFIR! Yüzde hesaplama yapılamaz.')
                continue
            
            diff_pct = ((val - med) / abs(med)) * 100
            
            print(f'\n{ratio_code.upper()}:')
            print(f'  Garanti: {val:.6f} ({val*100:.2f}%)')
            print(f'  Median:  {med:.6f} ({med*100:.2f}%)')
            print(f'  Fark:    ({val:.6f} - {med:.6f}) / {abs(med):.6f} * 100')
            print(f'         = {val - med:.6f} / {abs(med):.6f} * 100')
            print(f'         = {diff_pct:.1f}%')
            
            # Check if extreme
            if abs(diff_pct) > 100:
                print(f'  ⚠️  UYARI: Fark çok yüksek! Median çok düşük olabilir.')
                
                # Check if median is anomalous
                if abs(med) < 0.005:  # %0.5'ten küçük
                    print(f'  🚨 HATA: Sektör median ({med*100:.2f}%) çok düşük!')
                    print(f'      → Muhtemelen benchmark hesaplama hatası var.')

