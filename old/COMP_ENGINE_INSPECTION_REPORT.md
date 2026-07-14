# COMP Engine (Temel Analiz Uzmanı) - Detaylı İnceleme Raporu

**Tarih:** 28 Ocak 2026  
**İnceleme Konusu:** Finansal veri kalitesi, rasyo hesaplamaları ve sektör benchmarkları

---

## 🎯 Executive Summary

COMP Engine, 610 şirket ve 328,212 finansal tablo satırıyla geniş bir veri tabanına sahip. Ancak **kritik sorunlar** tespit edildi:

| Metrik | Değer | Durum |
|--------|-------|-------|
| Şirketler | 610 | ✅ Tam |
| Finansal Tablo Satırı | 328,212 | ✅ Tam |
| Company Ratios | **127** | ❌ **ÇOK DÜŞÜK** |
| Sector Benchmarks | **18** | ❌ **YETERSİZ** |

**Ana Sorun:** Rasyo hesaplaması ciddi şekilde eksik. 127 rasyo, 610 şirket için ~0.2 rasyo/şirket demek - bu kabul edilemez.

---

## 📊 1. Mali Tablolar Veri Kalitesi

### 1.1 Veri Dağılımı

| Finansal Grup | Şirket | Satır | Durum |
|---------------|--------|-------|-------|
| XI_29 (Endüstriyel) | 544 | 310,999 | ✅ %89 |
| UFRS_K (Bankacılık) | 18 | 17,213 | ✅ Bankalar |

### 1.2 Sektörel Dağılım

| Sektör | Şirket | Satır | % |
|--------|--------|-------|---|
| Tüketim & Perakende & Tekstil | 83 | 47,894 | 14.6% |
| Sanayi & Metal & Kimya | 72 | 41,438 | 12.6% |
| Gıda & İçecek & Tarım | 66 | 37,467 | 11.4% |
| GYO (Gayrimenkul) | 59 | 33,359 | 10.2% |
| Otomotiv & Savunma & Makine | 48 | 27,906 | 8.5% |
| Teknoloji & İletişim | 40 | 22,622 | 6.9% |
| Enerji | 39 | 22,622 | 6.9% |
| Holdingler | 38 | 22,040 | 6.7% |
| İnşaat & Yapı Malzemeleri | 29 | 16,450 | 5.0% |
| Turizm & Medya & Eğlence | 21 | 11,754 | 3.6% |
| Bankacılık & Finans | 14 | 10,669 | 3.3% |
| Ulaştırma & Lojistik | 18 | 10,552 | 3.2% |
| Diğer | 14 | 8,077 | 2.5% |
| Sağlık & İlaç | 13 | 7,642 | 2.3% |
| Sigortacılık | 4 | 6,544 | 2.0% |
| Spor | 4 | 1,176 | 0.4% |

**Değerlendirme:** Mali tablo verisi **mükemmel** - 16 sektör, 610 şirket kapsanmış.

### 1.3 Dönem Kapsama

| Dönem | Şirket | Satır |
|-------|--------|-------|
| 2026Q1 | 539 | 80,889 |
| 2025Q4 | 554 | 82,925 |
| 2025Q3 | 550 | 82,506 |
| 2025Q2 | 546 | 81,892 |

**Değerlendirme:** Son 4 çeyrek için veri mevcut. TTM hesaplamaları için yeterli.

---

## ⚠️ 2. Rasyo Hesaplama Sorunları

### 2.1 Mevcut Durum

**Beklenen:** 610 şirket × ~15 rasyo = **~9,150+ rasyo**  
**Gerçekleşen:** **127 rasyo** (%1.4 başarı oranı)

### 2.2 Rasyo Dağılımı

| Kategori | Adet | Beklenen | Fark |
|----------|------|----------|------|
| Profitability | 48 | ~2,000 | -97.6% |
| Leverage | 29 | ~1,200 | -97.6% |
| Liquidity | 24 | ~1,000 | -97.6% |
| Efficiency | 18 | ~800 | -97.7% |
| Valuation | 8 | ~500 | -98.4% |
| **Banking** | **0** | ~200 | **-100%** |

### 2.3 Rasyo Kodları Dağılımı

| Rasyo | Adet | Beklenen (610 şirket) |
|-------|------|----------------------|
| roe | 16 | 610 |
| current_ratio | 12 | 610 |
| acid_test_ratio | 12 | 610 |
| debt_to_equity | 11 | 610 |
| roa | 11 | 610 |
| receivables_turnover | 11 | 610 |
| net_debt_to_equity | 11 | 610 |
| ebitda_margin | 7 | 610 |
| asset_turnover | 7 | 610 |
| gross_margin | 7 | 610 |
| debt_ratio | 7 | 610 |
| net_margin | 7 | 610 |
| pb_ratio | 4 | 610 |
| pe_ratio | 4 | 610 |

**KRİTİK SORUN:** Bankacılık rasyoları (net_interest_margin, npl_ratio, capital_adequacy, loan_to_deposit) **HİÇ HESAPLANMADI**.

---

## 🔍 3. Kök Neden Analizi

### 3.1 Rasyo Hesaplama Sorunları

```python
# calculate_ratios_sync.py'deki sorunlar:

1. **TTM Veri Eksikliği:**
   - TTM hesaplaması için son 4 çeyrek verisi gerekiyor
   - Ancak 539-554 şirket 2026Q1 için veriye sahipken, sadece ~10-20 şirket için rasyo hesaplanmış

2. **Item Code Mapping Eksikliği:**
   - XI_29 için 28 item code maplenmiş (yetersiz)
   - UFRS_K için 47 item code maplenmiş (yeterli)
   - Gerekli item'lar maplenmemiş olabilir

3. **Financial Data Derivation:**
   - EBITDA = operating_income fallback (yanlış)
   - interest_earning_assets hesaplanmamış
   - total_debt derivation yetersiz
```

### 3.2 Benchmark Sorunları

| Sektör | Benchmark | N Peers | Reliability |
|--------|-----------|---------|-------------|
| Otomotiv & Savunma | 3 | 3 | LOW |
| Sanayi & Metal | 11 | 3 | LOW |
| Ulaştırma & Lojistik | 4 | 3 | LOW |

**SORUN:** Tüm benchmarklar `LOW` reliability ile 3 peers içeriyor. Bu, F5 filter'ın minimum peer sayısı olduğu için yeterli veri olmadığını gösteriyor.

---

## 🛠️ 4. Teknik Sorunlar

### 4.1 EBITDA Hesaplaması

```python
# MEVCUT (YANLIŞ):
ebitda = operating_income  # D&A eksik!

# DOĞRUSU:
ebitda = operating_income + depreciation + amortization
```

**Etki:** `ev_ebitda` ve `ebitda_margin` rasyoları hatalı.

### 4.2 Banking Rasyoları

```python
# Bankacılık için gerekli ama eksik:
- net_interest_margin → interest_earning_assets_avg yok
- loan_to_deposit → deposits + gross_loans var
- npl_ratio → non_performing_loans + gross_loans var
- capital_adequacy → risk_weighted_assets yok (TBB fallback kullanılıyor)
```

### 4.3 Item Code Mapping

**XI_29 için eksik mapping'ler:**
- Cash flow statement item'ları (4X serisi) → **HİÇ YOK**
- Depreciation & Amortization → **YOK**
- Interest expense/income detayı → **YOK**

---

## 📈 5. Pro-Level Olması İçin Gerekli İyileştirmeler

### 5.1 Kısa Vadeli (1 Hafta) - KRİTİK

| Öncelik | Görev | Etki |
|---------|-------|------|
| 1 | Rasyo hesaplama debug | +9,000 rasyo |
| 2 | EBITDA düzeltme | Valuation accuracy |
| 3 | Banking rasyoları | 18 banka için |
| 4 | Cash flow mapping | 30+ item |

### 5.2 Orta Vadeli (2-4 Hafta)

| Öncelik | Görev | Açıklama |
|---------|-------|----------|
| 1 | Data validation service | Cross-check balance sheet |
| 2 | Quality scoring | 0.0-1.0 completeness score |
| 3 | Restatement detection | Checksum comparison |
| 4 | Sector-specific ratios | REIT FFO, Insurance combined ratio |

### 5.3 Uzun Vadeli (1-3 Ay)

| Öncelik | Görev | Açıklama |
|---------|-------|----------|
| 1 | Peer group customization | User-defined peers |
| 2 | DuPont analysis | ROE decomposition |
| 3 | Credit scoring | Altman Z, Piotroski F |
| 4 | Historical trends | 5-year ratio trends |

---

## 🏦 6. Sektör-Özel Rasyo Gereksinimleri

### 6.1 Bankacılık (UFRS_K)

| Rasyo | Durum | Gerekli Veri |
|-------|-------|--------------|
| Net Interest Margin | ❌ Eksik | interest_earning_assets |
| Loan-to-Deposit | ✅ Hesaplanabilir | deposits, gross_loans |
| NPL Ratio | ✅ Hesaplanabilir | npl, gross_loans |
| Capital Adequacy | ⚠️ Fallback | risk_weighted_assets |
| Cost-to-Income | ✅ Hesaplanabilir | operating_expenses, total_income |

### 6.2 Sigortacılık (UFRS_S)

| Rasyo | Durum | Gerekli Veri |
|-------|-------|--------------|
| Loss Ratio | ✅ Var | claims, premiums |
| Expense Ratio | ✅ Var | expenses, premiums |
| Combined Ratio | ✅ Var | loss + expense |
| Investment Yield | ❌ Eksik | investment_income, investments |

### 6.3 GYO (XI_29 Özel)

| Rasyo | Durum | Gerekli Veri |
|-------|-------|--------------|
| NAV Discount | ⚠️ Kısmen | nav_per_share, market_price |
| Rental Yield | ⚠️ Kısmen | rental_income, property_value |
| FFO | ❌ Eksik | funds_from_operations |
| AFFO | ❌ Eksik | adjusted_ffo |

---

## 📋 7. Önerilen Aksiyon Planı

### Faz 1: Acil Düzeltmeler (Bu Hafta)

```bash
1. calculate_ratios_sync.py debug
   - Neden sadece 127 rasyo hesaplandı?
   - TTM data collection kontrol
   - Item code mapping validation

2. EBITDA calculation fix
   - Cash flow'dan D&A al
   - Eğer yoksa estimate et

3. Banking ratios activation
   - interest_earning_assets hesapla
   - Loan-to-deposit, NPL ratio çalıştır

4. Cash flow item mapping
   - 4A, 4B, 4C, 4D serisi kodları
```

### Faz 2: Kalite İyileştirmesi (Gelecek Hafta)

```bash
1. Data validation pipeline
   - Balance sheet: assets = liabilities + equity
   - Income statement: gross = revenue - cogs
   - Period-over-period sanity check

2. Quality scoring
   - Completeness: kaç item dolu?
   - Timeliness: ne kadar güncel?
   - Consistency: period farkları mantıklı mı?

3. Benchmark recalibration
   - MIN_PEERS_FOR_BENCHMARK = 3 → 5 yap
   - Winsorization parametreleri kontrol
   - Reliability scoring iyileştir
```

### Faz 3: Pro-Level Features (Gelecek Ay)

```bash
1. Sector-specific dashboards
2. Peer comparison tool
3. Historical trend analysis
4. AI-powered insights
```

---

## 🎯 8. Başarı Kriterleri

| Metrik | Mevcut | Hedef (1 Hafta) | Hedef (1 Ay) |
|--------|--------|-----------------|--------------|
| Company Ratios | 127 | 9,000+ | 12,000+ |
| Sector Benchmarks | 18 | 500+ | 1,000+ |
| Banking Ratios | 0 | 90+ | 180+ |
| Data Quality Score | N/A | 0.75+ | 0.90+ |
| Reliability HIGH | 0% | 30% | 60% |

---

## 📝 Sonuç

COMP Engine'in **veri tabanı mükemmel** (328K satır, 610 şirket) ancak **rasyo hesaplama motoru çalışmıyor**. Bu, item code mapping eksikliği, TTM data collection sorunları ve banking-specific hesaplamaların aktif edilmemesinden kaynaklanıyor.

**Acil eylem gerekiyor:**
1. Rasyo hesaplama debug
2. EBITDA düzeltme
3. Banking rasyoları aktifleştirme
4. Cash flow statement mapping

Bu düzeltmeler yapıldığında, sistem pro-level temel analiz için hazır hale gelecektir.

---

**Raporu Hazırlayan:** Kiro AI Assistant  
**Tarih:** 28 Ocak 2026
