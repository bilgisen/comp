# HissePro Rating Sistem Raporu

## Özet

Şirket skorlama sistemi başarıyla kuruldu ve çalıştırıldı. Sistem, her şirket için 0-100 aralığında iki bağımsız skor üretiyor:

- **score_sektor**: Şirketin kendi sektöründeki konumu
- **score_genel**: Şirketin tüm BIST içindeki konumu

## Sonuçlar (2026Q1)

| Metrik | Değer |
|--------|-------|
| Toplam şirket | 539 |
| Sektör skoru olan | 522 |
| Genel skoru olan | 520 |
| Ort. sektör skoru | 52.00 |
| Ort. genel skoru | 49.72 |
| Max sektör skoru | 95.11 |
| Min sektör skoru | 18.99 |

## Sektör Bazlı Skorlar

| Sektör | Şirket Sayısı | Ort. Skor | Max Skor |
|--------|---------------|-----------|----------|
| GYO | 55 | 62.9 | 85.8 |
| Bankacılık & Finans | 12 | 59.1 | 65.9 |
| Diğer | 14 | 56.5 | 80.8 |
| Sağlık & İlaç | 13 | 54.9 | 65.0 |
| Teknoloji & İletişim | 38 | 53.8 | 90.4 |
| Holdingler | 30 | 53.5 | 95.1 |

## Top 10 Şirketler (Sektör Skoru)

| Ticker | Şirket | Sektör Skoru | Genel Skoru | Güvenilirlik |
|--------|--------|--------------|-------------|--------------|
| BRYAT | Borusan Yatırım | 95.1 | 77.0 | MEDIUM |
| METRO | Metro Tic. Mali Yat. | 90.9 | 73.3 | MEDIUM |
| INVES | Investco Holding | 90.8 | 65.3 | MEDIUM |
| NETCD | Netcad Yazılım | 90.4 | 72.0 | MEDIUM |
| MERIT | Merit Turizm Yatırım | 87.7 | 59.1 | MEDIUM |
| YGGYO | Yeni Gimat GYO | 85.8 | 59.3 | MEDIUM |
| TDGYO | Trend GYO | 84.0 | 75.5 | MEDIUM |
| LINK | Link Bilgisayar | 83.7 | 70.7 | MEDIUM |
| SVGYO | Savur GYO | 83.4 | 59.8 | MEDIUM |
| ORGE | ORGE Enerji Elektrik | 82.0 | 63.3 | MEDIUM |

## Mimari

### Modeller
- `models/score.py`: CompanyScore, CompanyScoreDetail, GlobalBenchmark

### Servisler
- `services/scoring/ratio_scorer.py`: Sigmoid tabanlı skor algoritması
- `services/scoring/pillar_config.py`: Sektöre özgü pillar konfigürasyonları
- `services/scoring/engine.py`: Ana skor hesaplama motoru
- `services/scoring/worker.py`: Batch işleme

### API Endpoint'leri
- `GET /api/v1/scores/{ticker}`: Tek şirket skoru
- `GET /api/v1/scores/`: Liste halinde skorlar
- `GET /api/v1/scores/leaderboard/sektor`: Sektör liderleri
- `GET /api/v1/scores/leaderboard/genel`: Genel liderler
- `GET /api/v1/scores/compare/{tickers}`: Karşılaştırma
- `POST /api/v1/scores/compute/{period_key}`: Manuel tetikleme

## Pillar Yapısı

### XI_29 (Genel Sektörler)
- **Kârlılık** (%40): gross_margin, operating_margin, net_margin, ebitda_margin, roe
- **Finansal** (%35): current_ratio, acid_test_ratio, debt_ratio, net_debt_to_equity
- **Verimlilik** (%25): asset_turnover

### Bankacılık (CAMELS-Lite)
- **Kârlılık** (%35): roe, roa, net_interest_margin
- **Verimlilik** (%25): cost_income_ratio
- **Varlık Kalitesi** (%25): npl_ratio
- **Sermaye/Likidite** (%15): capital_adequacy, loan_to_deposit

### Sigortacılık
- **Kârlılık** (%35): roe, net_margin, roa
- **Teknik Performans** (%40): combined_ratio, loss_ratio, expense_ratio
- **Değerleme** (%25): pb_ratio

## Algoritma

### Sigmoid Tabanlı Percentile Skoru
```
1. IQR ile normalize edilmiş Z-skoru hesapla
2. Sigmoid fonksiyonu uygula: f(z) = 100 / (1 + e^(-k*z))
3. Reliability dampening uygula
```

### Reliability Dampening
- HIGH (n>=10): dampening yok
- MEDIUM (5-9): %20 medyana yaklaştır
- LOW (3-4): %45 medyana yaklaştır
- INSUFFICIENT (<3): skor yok

## Kullanım

```bash
# Tabloları oluştur
python create_score_tables.py --create-tables

# Veri durumunu kontrol et
python create_score_tables.py --check-data

# Skorları hesapla
python create_score_tables.py --score

# API'yi başlat
python main.py
```

## Sonraki Adımlar

1. Market cap verisi eklendiğinde P/E, P/B skorları da hesaplanacak
2. Geçmiş dönemler için de skorlar hesaplanabilir
3. Frontend'de skor görselleştirme eklenebilir
4. Skor değişim trendleri takip edilebilir
