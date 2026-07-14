# Bootstrap Tüm Sektörler için Execution Plan

## Mevcut Durum (27 Haziran 2026)

### ✅ Tamamlanan
- Bankacılık & Finans: 57 şirket, 10,669 rows
- Total financial statements: 18,313 rows
- Total companies: 610

### ⚠️ Eksik
- Ratio Calculation: Transaction error
- Sector Benchmarks: Eksik
- Diğer 13 sektör: Fetch edilmemiş

## Execution Plan

### Option 1: Full Bootstrap (Tüm Sektörler)
```bash
python bootstrap_comp_engine.py --all
```

**Duration:** ~60 dakika (610 şirket)
**Expected Results:**
- 600K+ financial statement rows
- 40K+ ratios
- 1K+ benchmarks

### Option 2: Sektör Sektör
Her sektör için ayrı ayrı:
```bash
# 1. Bankacılık & Finans (✅ TAMAMLANDI)
python bootstrap_comp_engine.py --sector "Bankacılık & Finans"

# 2. Sanayi & Metal & Kimya
python bootstrap_comp_engine.py --sector "Sanayi & Metal & Kimya"

# 3. Teknoloji & İletişim
python bootstrap_comp_engine.py --sector "Teknoloji & İletişim"

# 4. Enerji & Altyapı
python bootstrap_comp_engine.py --sector "Enerji & Altyapı"

# 5. GYO
python bootstrap_comp_engine.py --sector "GYO"

# 6. Gıda & İçecek & Tarım
python bootstrap_comp_engine.py --sector "Gıda & İçecek & Tarım"

# 7. Tüketim & Perakende & Tekstil
python bootstrap_comp_engine.py --sector "Tüketim & Perakende & Tekstil"

# 8. Ulaştırma & Lojistik
python bootstrap_comp_engine.py --sector "Ulaştırma & Lojistik"

# 9. Otomotiv & Savunma & Makine
python bootstrap_comp_engine.py --sector "Otomotiv & Savunma & Makine"

# 10. İnşaat & Yapı Malzemeleri
python bootstrap_comp_engine.py --sector "İnşaat & Yapı Malzemeleri"

# 11. Turizm & Medya & Eğlence
python bootstrap_comp_engine.py --sector "Turizm & Medya & Eğlence"

# 12. Sağlık & İlaç
python bootstrap_comp_engine.py --sector "Sağlık & İlaç"

# 13. Holdingler
python bootstrap_comp_engine.py --sector "Holdingler"

# 14. Sigortacılık
python bootstrap_comp_engine.py --sector "Sigortacılık"
```

## Ratio Calculation Issue

**Problem:** Transaction abort during ratio calculation
```
asyncpg.exceptions.InFailedSQLTransactionError: current transaction is aborted
```

**Root Cause:** Database connection/transaction management issue

**Solution:** 
1. Check async/sync session usage
2. Implement proper transaction rollback
3. Add connection pooling timeout settings

## Recommendation

**ÖNERİ:** Önce ratio calculation bug'ını fix edelim, sonra tüm sektörleri fetch edelim.

**Steps:**
1. Fix `_phase_calculate_ratios()` transaction handling
2. Test with single company
3. Run full bootstrap with --all flag

**Yoksa devam edelim mi tüm sektörleri fetch etmeye?**
