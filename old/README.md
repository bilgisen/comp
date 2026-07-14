# 🏗️ HissePro Financial Analysis Engine (COMP)

Pro-level finansal analiz motoru. İş Yatırım API'sinden mali tabloları çekerek 50+ finansal rasyo hesaplar, sektör karşılaştırmaları yapar ve AI chatbot'a zengin context sağlar.

## 🎯 Özellikler

### Temel İşlevler
- 📊 **Mali Tablo Çekimi**: İş Yatırım API entegrasyonu (rate-limited, diff-based)
- 🧮 **Rasyo Hesaplama**: 50+ finansal rasyo (sektöre özel konfigürasyonlar)
- 📈 **Sektör Benchmarkları**: F1-F5 filtreli medyan hesaplama
- 🤖 **AI Context Builder**: Gemini için optimize edilmiş finansal context
- ⚡ **Real-time Updates**: Event-driven hesaplama sistemi

### Teknik Özellikler
- 🚀 **FastAPI**: Async/await ile yüksek performans
- 🐘 **PostgreSQL**: Yapılandırılmış finansal veri depolama
- 🔴 **Redis/Valkey**: Akıllı önbellekleme
- 📋 **APScheduler**: Otomatik veri çekme
- 🛡️ **Type Safety**: Pydantic modelleri
- 📊 **Monitoring**: Health checks + metrics

## 📊 Desteklenen Sektörler

| Ana Sektör | Financial Group | Özel Rasyolar |
|------------|----------------|---------------|
| **Bankacılık & Finans** | UFRS_K | NIM, Kredi/Mevduat, NPL, Sermaye Yeterlilik |
| **Sigortacılık** | UFRS_S | Hasar/Prim, Birleşik Oran |
| **GYO** | XI_29 | NAV İskonto, Kira Getirisi |
| **Enerji & Altyapı** | XI_29 | Standart + sektor sınırları |
| **Teknoloji & İletişim** | XI_29 | Yüksek F/K toleransı |
| **Diğer 9 Sektör** | XI_29 | Sektöre özel ekonomik sınırlar |

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Repository klonlama
cd comp

# Python sanal ortamı (önerilir)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya Windows:
venv\Scripts\activate

# Bağımlılıkları yükleme
pip install fastapi==0.104.1 uvicorn sqlalchemy==2.0.23 asyncpg redis
pip install httpx apscheduler scipy numpy pydantic-settings python-dotenv
```

### 2. Ortam Yapılandırması

```bash
# .env dosyası oluşturma
copy .env.example .env

# .env dosyasını düzenleme (gerekli ayarlar)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/hissepro_comp
REDIS_URL=redis://localhost:6379/0
```

### 3. Veritabanı Kurulumu

```bash
# PostgreSQL veritabanı oluşturma
createdb hissepro_comp

# Redis başlatma (Docker)
docker run -d --name redis -p 6379:6379 redis:alpine

# Tabloları otomatik oluşturulur (ilk çalıştırmada)
```

### 4. Sunucu Başlatma

```bash
# Geliştirme sunucusu
python main.py

# Veya uvicorn ile
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

🎉 **API hazır!** → http://localhost:8000/docs

### 5. Sistem Test

```bash
# Sağlık kontrolü
curl http://localhost:8000/health

# API dokümantasyonu
open http://localhost:8000/docs
```

## 📡 API Kullanımı

### Temel Endpointler

```bash
# Şirket rasyoları
GET /api/v1/companies/THYAO/ratios

# Sektör karşılaştırması  
GET /api/v1/companies/THYAO/compare?compare_to=sector

# Sektör benchmarkları
GET /api/v1/sectors/Teknoloji%20%26%20İletişim/benchmarks

# AI Context (chatbot için)
GET /api/v1/ai/context/THYAO?context_type=comprehensive
```

### Örnek Response (Şirket Rasyoları)

```json
{
  "ticker": "THYAO",
  "company_name": "Türk Hava Yolları",
  "sector": "Ulaştırma & Lojistik",
  "period": "2026Q1",
  "ratios": {
    "current_ratio": {
      "value": 0.89,
      "sector_comparison": {
        "sector_median": 1.23,
        "company_percentile": 25,
        "vs_sector": "below",
        "n_peers": 12,
        "reliability": "HIGH"
      },
      "data_quality_score": 0.95
    },
    "roe": {
      "value": 0.156,
      "is_ttm": true,
      "sector_comparison": {
        "sector_median": 0.134,
        "company_percentile": 78
      }
    }
  }
}
```

## 🔧 Geliştirici Kılavuzu

### Yeni Rasyo Ekleme

```python
# services/ratio_calculator.py içinde

"new_ratio_code": RatioConfig(
    code="new_ratio_code",
    formula=lambda d: d.get("numerator", 0) / d.get("denominator", 1) if d.get("denominator", 0) != 0 else None,
    type="instant",  # veya "ttm"
    description="Yeni Rasyo = Pay / Payda",
    category="profitability"
)
```

### Item Code Mapping

```python
# services/item_code_mapper.py içinde UFRS_K_MAPPINGS veya XI_29_MAPPINGS

"YENİ_KOD": "semantic_name"  # İş Yatırım API'den gelen kod -> anlam
```

### Sektöre Özel Konfigürasyon

```python
# services/ratio_calculator.py içinde SECTOR_RATIOS

"Yeni Sektör": {
    "özel_rasyo": RatioConfig(...),
    **DEFAULT_RATIOS  # Genel rasyolar da dahil
}
```

## 🗄️ Veritabanı Şeması

### Ana Tablolar

```sql
companies                 -- Şirket metadata
├── financial_statements_raw  -- Ham mali tablo verileri
├── company_ratios           -- Hesaplanan rasyolar
└── fetch_logs              -- API çekim audit log

sector_benchmarks        -- Sektör medyanları
└── sector_benchmark_companies  -- Dahil/hariç şirketler (audit)

item_code_mappings       -- İş Yatırım kod → semantik mapping
ai_context_cache         -- AI context önbelleği
```

### İndeksler (Performance)

- `companies.ticker` (UNIQUE)
- `companies.sector_main + is_active`
- `company_ratios.ticker + ratio_code`
- `fetch_logs.is_new_data + fetched_at`

## 📊 F1-F5 Filtre Pipeline

Sektör medyanı hesaplarken güvenilirlik için 5-aşamalı filtre:

```
Ham Veri (N=50 şirket)
  │
  ▼ F1: NULL/Infinite → (N=45)
  ▼ F2: Min 3 dönem verisi → (N=38) 
  ▼ F3: Ekonomik sınırlar → (N=32)
  ▼ F4: Winsorization P5-P95 → (N=30)
  ▼ F5: Min 3 peer kontrolü → ✅ Güvenilir medyan
```

**Güvenilirlik Seviyeleri:**
- 🟢 **HIGH**: n≥10 peer
- 🟡 **MEDIUM**: 5≤n<10 peer  
- 🔶 **LOW**: 3≤n<5 peer
- 🔴 **INSUFFICIENT**: n<3 peer (hesaplanmaz)

## 🕐 Otomatik Çekim Sistemi

### 3-Katmanlı Scheduler

```bash
Layer 1: Her gün 07:00 TSİ
         ├─ KAP raporlama penceresi içindeki şirketler
         └─ Çeyrek sonu + 75 gün

Layer 2: Pazar 04:00 TSİ  
         ├─ Tüm aktif şirketler (safety net)
         └─ Kaçırılan şirketler için

Layer 3: Manuel tetikleme
         └─ Admin UI üzerinden
```

### Rate Limiting (İş Yatırım'a saygılı)

- ⏱️ **20 req/min** (dakikada maksimum)
- 🔄 **3 sn** gecikme (jitter ile 2.5-4.0)
- 📦 **50 şirket/batch** (sonra 2 dk mola)
- 🔄 **3x retry** (429/503 hatalar için)

## 🤖 AI Chatbot Entegrasyonu

### Context Builder

```python
# Gemini için optimize edilmiş Türkçe context
context = await AIContextBuilder(db).build_context("THYAO", "comprehensive")

# Context içeriği:
# - 📊 Temel bilgiler (şirket, sektör, piyasa değeri)
# - 💰 Likidite rasyoları (sektör karşılaştırmalı)
# - 📈 Kârlılık rasyoları (trend analiziyle)
# - ⚖️ Kaldıraç rasyoları (risk değerlendirmeli)
# - 🎯 Değerleme rasyoları (sektör persentilleri)
# - ⚠️ Risk uyarıları ve disclaimer
```

### Hono Entegrasyonu

```javascript
// hono/src/lib/fundamental-context-builder.js
const fundamentalContext = await fetch(
  `${COMP_API_URL}/api/v1/ai/context/${ticker}?context_type=comprehensive`
);
```

## 🚀 Production Deployment

### FastAPI Cloud

```bash
# 1. Push to repository
git add . && git commit -m "COMP Engine ready"

# 2. Deploy to FastAPI Cloud
# Proje URL: https://comp-[hash].fastapicloud.dev

# 3. Environment variables ayarlama
# Dashboard > Settings > Environment Variables
```

### Environment Variables (Production)

```env
DATABASE_URL=postgresql+asyncpg://user:pass@production-db/comp
REDIS_URL=redis://production-redis:6379/0
ENABLE_SCHEDULER=true
SECRET_KEY=production-secret-key
SENTRY_DSN=https://sentry-dsn
```

### Health Monitoring

```bash
# Health check
curl https://comp-hash.fastapicloud.dev/health

# System health (detailed)
curl https://comp-hash.fastapicloud.dev/api/v1/admin/system/health

# Fetch status
curl https://comp-hash.fastapicloud.dev/api/v1/admin/fetch/status
```

## 📈 Performance Benchmarks

### Hedeflenen Performans

| Metrik | Target | Açıklama |
|--------|--------|----------|
| **API Response** | <100ms | Önbellekli veriler için |
| **Rasyo Hesaplama** | <5sn | 50 rasyo/şirket |
| **Mali Tablo Çekimi** | <30sn | İş Yatırım API |
| **Sektör Medyanı** | <10sn | 50 şirket/sektör |
| **AI Context** | <2sn | Önbellekli context |

### Monitoring Metrikleri

- 📊 Request latency (P95, P99)
- 🔴 Error rate (4xx, 5xx)
- 📈 Cache hit rate (Redis)
- 🗄️ Database connections
- 📥 İş Yatırım API rate limiting

## 🧪 Testing

### Unit Tests

```bash
# Tüm testleri çalıştırma
pytest

# Specific module
pytest tests/test_ratio_calculator.py

# Coverage report
pytest --cov=services tests/
```

### Integration Tests

```bash
# Database integration
pytest tests/integration/test_database.py

# API endpoints
pytest tests/integration/test_api.py

# İş Yatırım client
pytest tests/integration/test_isyatirim_client.py
```

### Load Testing

```bash
# API load test (locust kullanarak)
pip install locust
locust -f tests/load/api_load_test.py --host=http://localhost:8000
```

## 🔧 Troubleshooting

### Yaygın Sorunlar

**1. Database Connection Error**
```bash
# PostgreSQL çalışıyor mu?
sudo systemctl status postgresql

# Connection string doğru mu?
echo $DATABASE_URL
```

**2. Redis Connection Error**
```bash
# Redis çalışıyor mu?  
redis-cli ping

# Connection string doğru mu?
echo $REDIS_URL
```

**3. İş Yatırım API Timeout**
```bash
# Network connectivity
curl -I https://www.isyatirim.com.tr

# Rate limiting kontrolü
grep "Rate limit" logs/comp.log
```

**4. Missing Item Code Mappings**
```bash
# Mapping coverage kontrolü
curl http://localhost:8000/api/v1/admin/mappings/validate/THYAO

# Yeni mappingler ekleme
# services/item_code_mapper.py düzenleme gerekli
```

### Debug Logging

```python
# Debug modunu açma (.env dosyasında)
DEBUG=true

# Specific logger
import logging
logging.getLogger("services.ratio_calculator").setLevel(logging.DEBUG)
```

## 📚 İleri Seviye Kullanım

### Custom Sektör Tanımlama

```python
# Company model'de yeni sektör
company.sector_main = "Özel Sektör"

# RatioCalculator'da özel konfigürasyon
SECTOR_RATIOS["Özel Sektör"] = {
    "özel_rasyo": RatioConfig(...),
}
```

### Webhook Entegrasyonu

```python
# Yeni veri geldiğinde webhook tetikleme
@router.post("/webhooks/data-updated")
async def handle_data_update(payload: dict):
    # Downstream sistemlere bildirim
    await notify_hono_orchestrator(payload)
    await invalidate_frontend_cache(payload)
```

### Multi-Currency Support

```python
# İleri seviye: USD mali tabloları
result = await isyatirim_client.fetch_mali_tablo("THYAO", currency="USD")
```

## 🤝 Katkıda Bulunma

### Development Workflow

```bash
# 1. Feature branch oluşturma
git checkout -b feature/new-ratio

# 2. Değişiklikleri yapma
# services/, models/, routers/ düzenleme

# 3. Test yazma
# tests/ altında unit test ekleme

# 4. Code quality check
black . && ruff check .

# 5. Test çalıştırma
pytest

# 6. Commit & Push
git commit -m "feat: Add new profitability ratio"
git push origin feature/new-ratio
```

### Code Style

- **Black**: Code formatting
- **Ruff**: Linting  
- **Type hints**: Tüm fonksiyonlar
- **Docstrings**: Public API'ler
- **Async/await**: I/O operations

## 📄 Lisans

MIT License - Internal use only

## 🆘 Destek

- 📖 **Dokümantasyon**: Bu README + kod yorumları
- 🐛 **Bug Report**: GitHub Issues
- 💬 **Soru**: Team chat channel
- 📧 **İletişim**: team@hissepro.com

---

**🎯 Hedef**: Türkiye'nin en kapsamlı finansal analiz motoru

**⚡ Status**: Beta - Production Ready**

**🚀 Next**: Hono entegrasyonu + Frontend bağlantısı**

## 📦 GitHub Deployment

### Git Kurulumu ve Push

```bash
# 1. Git'i başlat
git init

# 2. .gitignore ayarları otomatik (dosya mevcut)

# 3. Tüm dosyaları ekle
git add .

# 4. İlk commit
git commit -m "feat: HissePro COMP Engine v2.0.0 - Pro-level financial analysis engine"

# 5. GitHub repository oluştur (manuel adım)
# GitHub'da yeni repo: hissepro-comp-engine

# 6. Remote ekle
git remote add origin https://github.com/[kullanıcı-adı]/hissepro-comp-engine.git

# 7. Branch oluştur
git branch -M main

# 8. Push et
git push -u origin main
```

### Repository Yapısı

```
hissepro-comp-engine/
├── .gitignore               # Ignore rules
├── .env.example            # Environment template
├── README.md               # This documentation
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project config
│
├── core/                   # Core infrastructure
│   ├── config.py          # Settings management
│   ├── database.py        # PostgreSQL integration
│   ├── cache.py           # Redis cache manager
│   └── __init__.py
│
├── models/                 # Database models
│   ├── company.py         # Company data models
│   ├── financial.py       # Financial statement models
│   ├── benchmark.py       # Sector benchmark models
│   └── __init__.py
│
├── services/              # Business logic services
│   ├── isyatirim_client.py    # İş Yatırım API client
│   ├── ratio_calculator.py    # Financial ratio calculator
│   ├── sector_benchmarks.py   # Sector benchmark service
│   ├── comparison_service.py  # Company comparison engine
│   ├── trend_analysis.py      # Historical trend analysis
│   ├── ai_context_builder.py  # AI context generator
│   ├── scheduler.py           # Automated data fetching
│   └── __init__.py
│
├── routers/               # API endpoints
│   ├── companies.py      # Company endpoints
│   ├── sectors.py        # Sector endpoints
│   ├── admin.py          # Admin endpoints
│   ├── ai_context.py     # AI context endpoints
│   └── __init__.py
│
└── documentation/        # Project documentation
    ├── mali_tablo_sistemi_talimat.md
    └── hissepro_temel_analiz_ozet.md
```

### CI/CD için Öneriler

```yaml
# GitHub Actions (.github/workflows/deploy.yml)
name: Deploy HissePro COMP

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Lint
      run: |
        pip install black ruff
        black --check .
        ruff check .
    - name: Test
      run: |
        python -m pytest tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to FastAPI Cloud
      run: |
        # FastAPI Cloud deployment commands
        echo "Deployment to FastAPI Cloud"
```

### Production Ready Features

- ✅ **Containerization**: `Dockerfile` hazır
- ✅ **Environment Management**: `.env.example` template
- ✅ **Dependency Management**: `requirements.txt` & `pyproject.toml`
- ✅ **Security**: Secret management ready
- ✅ **Monitoring**: Health checks integrated
- ✅ **Caching**: Redis/Valkey optimized
- ✅ **Scheduling**: APScheduler integrated
- ✅ **API Documentation**: OpenAPI/Swagger auto-generated

### Deployment Options

1. **FastAPI Cloud** (Önerilen)
   ```bash
   # FastAPI Cloud CLI kurulumu
   pip install fastapi-cloud
   
   # Deploy
   fastapi-cloud deploy
   ```

2. **Docker**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **Railway/Heroku**
   - Procfile hazır
   - Environment variables management

### License

MIT License - Internal use only

### Support

- 📧 team@hissepro.com
- 📖 GitHub Issues
- 💬 Team chat channel

---

**🎯 Production Ready HissePro COMP Engine** - Türkiye'nin en kapsamlı finansal analiz motoru!