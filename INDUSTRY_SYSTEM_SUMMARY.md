# HissePro Industry System - Implementation Summary

## Overview

Yeni sektör sistemi **21 high-quality industry** (≥10 şirket) ile daha güvenilir peer karşılaştırmaları sağlar.

## API Endpoints

### ✅ NEW: Industry Endpoints (Recommended)

```
GET /api/v1/sectors/industries
→ 28 industry listesi (21 high-quality)

GET /api/v1/sectors/industries/{slug}
→ Industry detayı + şirket listesi
Örnek: /api/v1/sectors/industries/bankacilik

GET /api/v1/sectors/industries/{slug}/benchmarks
→ Industry için benchmark medyanları
```

### 🔄 LEGACY: Sector Endpoints (Backward Compatible)

```
GET /api/v1/sectors/
→ 14 broad sector (eski sistem - backward compatibility)

GET /api/v1/sectors/{sector}/companies
→ Şirket listesi (eski sistem)

GET /api/v1/sectors/{sector}/benchmarks
→ Benchmark verileri (eski sistem)
```

## Industry List (28 Total, 21 High-Quality)

### 🟢 HIGH Reliability (≥10 şirket)

| Industry | Şirket | Slug | Açıklama |
|----------|--------|------|----------|
| Gıda | 59 | `gida` | Gıda + Meşrubat birleştirildi |
| GYO | 58 | `gyo` | Gayrimenkul yatırım ortaklıkları |
| Holdingler | 38 | `holdingler` | Holding şirketler |
| Teknoloji | 30 | `teknoloji` | Teknoloji + İletişim |
| Elektrik Üretim | 28 | `elektrik-uretim` | Elektrik üretim şirketleri |
| Tekstil | 27 | `tekstil` | Tekstil entegre + terbiye |
| İnşaat Malzemeleri | 24 | `insaat-malzemeleri` | İnşaat + cam + mineral |
| Demir-Çelik | 23 | `demir-celik` | Demir-çelik temel + döküm |
| Kimya | 19 | `kimya` | Kimyasal ürünler |
| Yatırım Ortaklıkları | 17 | `yatirim-ortakliklari` | Yatırım ortaklıkları |
| Çimento | 16 | `cimento` | Çimento üreticileri |
| Bankacılık | 16 | `bankacilik` | **Sadece bankalar** (faktoring/leasing ayrı) |
| Kağıt | 15 | `kagit` | Kağıt ürünleri |
| Ulaştırma-Lojistik | 15 | `ulastirma-lojistik` | Ulaştırma + lojistik |
| Perakende | 14 | `perakende` | Perakende ticaret |
| Sağlık | 13 | `saglik` | Sağlık + ilaç |
| Turizm | 12 | `turizm` | Turizm işletmeleri |
| Otomotiv Yan Sanayi | 11 | `otomotiv-yan-sanayi` | Otomotiv parçaları |
| Finansal Kiralama | 11 | `finansal-kiralama` | Faktoring + leasing |
| Aracı Kurumlar | 10 | `araci-kurumlar` | Aracı kurumlar |
| **Diğer** | 109 | `diger` | Çeşitli sektörler |

### 🟡 MEDIUM Reliability (5-9 şirket)

| Industry | Şirket | Slug |
|----------|--------|------|
| Tüketim Elektroniği | 9 | `tuketim-elektronigi` |
| Otomotiv | 8 | `otomotiv` |
| Medya | 8 | `medya` |
| Sigortacılık | 6 | `sigortacilik` |
| Elektrik Dağıtım | 5 | `elektrik-dagitim` |

### 🔴 LOW Reliability (<5 şirket)

| Industry | Şirket | Slug |
|----------|--------|------|
| Savunma Sanayi | 4 | `savunma-sanayi` |
| Spor | 4 | `spor` |

---

## Frontend Implementation Guide

### 1. Ana Sayfa - Sektör Listesi

**Endpoint:** `GET /api/v1/sectors/industries`

**Tanstack Query Example:**
```typescript
const { data } = useQuery({
  queryKey: ['industries'],
  queryFn: () => fetch('/api/v1/sectors/industries').then(r => r.json())
})

// data.industries array döner, her biri:
{
  name: "Bankacılık",
  slug: "bankacilik",
  total_companies: 16,
  active_companies: 14,
  reliability: "HIGH",
  min_peers_for_benchmark: 3
}
```

**Display:**
- Kartlar halinde göster
- Badge ile reliability (HIGH=yeşil, MEDIUM=sarı, LOW=kırmızı)
- Şirket sayısını göster
- Click → `/sektorler/{slug}` sayfasına git

### 2. Sektör Detay Sayfası

**URL Pattern:** `/sektorler/{slug}`
Örnek: `/sektorler/bankacilik`

**Endpoints:**
```typescript
// Sektör bilgisi + şirket listesi
GET /api/v1/sectors/industries/{slug}

// Benchmark verileri
GET /api/v1/sectors/industries/{slug}/benchmarks?period=2026Q1
```

**Gösterilecekler:**
- Industry adı + şirket sayısı
- Reliability badge
- Şirket listesi (score'a göre sıralı)
- Her şirket için: isim, ticker, score, percentile

### 3. Chatbot Context

**Context Data:**
```json
{
  "page_type": "industry_detail",
  "industry": "Bankacılık",
  "total_companies": 16,
  "reliability": "HIGH",
  "companies": ["AKBNK", "GARAN", "HALKB", ...],
  "benchmarks_available": true,
  "peer_comparison_quality": "Yüksek - 16 banka karşılaştırılıyor"
}
```

**Chatbot Prompts:**
```
- "Bu sektörde kaç şirket var?" → 16 şirket (14'ü aktif skorlu)
- "Sektör medyanları güvenilir mi?" → Evet, HIGH reliability (16 peer)
- "En iyi şirket hangisi?" → Score'a göre sırala
- "Sektör ortalaması nedir?" → Benchmark API'den getir
```

---

## Cache Strategy

### Redis Keys

```
# Industry list (1 hour TTL)
industries:list:2026Q1

# Industry detail (30 min TTL)
industry:{slug}:detail

# Industry benchmarks (1 hour TTL)
industry:{slug}:benchmarks:2026Q1

# Company scores in industry (30 min TTL)
industry:{slug}:scores:2026Q1
```

### Invalidation Rules

```python
# Şirket skoru güncellendiğinde
→ Invalidate: industry:{slug}:scores:{period}
→ Invalidate: industry:{slug}:detail

# Benchmark hesaplandığında
→ Invalidate: industry:{slug}:benchmarks:{period}

# Yeni period başladığında
→ Invalidate: industries:list:*
→ Invalidate: industry:*:benchmarks:*
```

---

## Migration Notes

### Database

- ✅ `companies.industry` column eklendi
- ✅ 609 şirket map edildi
- ✅ 21 high-quality industry oluşturuldu

### Backend

- ✅ `SectorBenchmarkService` industry destekliyor
- ✅ Alt-sektör filtreleme (Bankacılık, Ulaştırma) korundu
- ✅ API endpoints eklendi (backward compatible)

### Frontend (TODO)

- [ ] Ana sayfa: `/sektorler` → Industry kartları
- [ ] Detay sayfa: `/sektorler/{slug}` → Industry detayı
- [ ] Tanstack Query hooks
- [ ] Cache implementasyonu
- [ ] Chatbot context güncellemesi

---

## Testing

```bash
# Industry listesi
curl https://comp-ef958063.fastapicloud.dev/api/v1/sectors/industries

# Bankacılık detayı
curl https://comp-ef958063.fastapicloud.dev/api/v1/sectors/industries/bankacilik

# Bankacılık benchmarks
curl https://comp-ef958063.fastapicloud.dev/api/v1/sectors/industries/bankacilik/benchmarks
```

---

## Benefits

✅ **Daha İyi Peer Karşılaştırmaları:** 21 high-quality industry (hepsi ≥10 şirket)  
✅ **Bankacılık Düzeltildi:** Artık sadece bankalar karşılaştırılıyor (faktoring/leasing ayrı)  
✅ **İstatistiksel Güvenilirlik:** Medyanlar için yeterli peer sayısı  
✅ **Backward Compatible:** Eski API endpoints hala çalışıyor  
✅ **Ölçeklenebilir:** Yeni industry'ler kolayca eklenebilir

---

## Next Steps

1. **Frontend Implementation** (2-3 saat)
   - Industry listesi sayfası
   - Industry detay sayfası
   - Tanstack Query hooks

2. **Cache Implementation** (1 saat)
   - Redis keys
   - Invalidation logic

3. **Chatbot Context** (30 dakika)
   - Context data preparation
   - Prompt updates

4. **Benchmark Recalculation** (Background)
   - Industry-based benchmarks
   - Test with Garanti Bankası AI report

---

**Status:** Backend ✅ Complete | Frontend ⏳ Pending | Cache ⏳ Pending
