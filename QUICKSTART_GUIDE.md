# 🚀 HissePro COMP Engine - Hızlı Başlangıç Kılavuzu

Bu kılavuz, COMP Engine'i 15 dakikada çalışır hale getirmeniz için hazırlanmıştır.

---

## ✅ Ön Gereksinimler

- ✅ Python 3.11+ kurulu
- ✅ Docker Desktop kurulu (PostgreSQL ve Redis için)
- ✅ Git (opsiyonel)

---

## 📦 1. Docker Servisleri Başlat (5 dakika)

### PostgreSQL (Veritabanı)

```powershell
docker run -d `
  --name hissepro-postgres `
  -e POSTGRES_DB=hissepro_comp `
  -e POSTGRES_USER=comp_user `
  -e POSTGRES_PASSWORD=secure_password `
  -p 5432:5432 `
  postgres:15-alpine
```

**Test et:**
```powershell
docker logs hissepro-postgres
# "database system is ready to accept connections" görmeli
```

---

### Redis (Cache)

```powershell
docker run -d `
  --name hissepro-redis `
  -p 6379:6379 `
  redis:7-alpine
```

**Test et:**
```powershell
docker exec -it hissepro-redis redis-cli ping
# Beklenen: PONG
```

---

## ⚙️ 2. Environment Konfigürasyonu (3 dakika)

### .env Dosyası Oluştur

```powershell
# comp klasörüne git
cd c:\Users\ASUS\hp\comp

# .env.example'ı kopyala
copy .env.example .env
```

### .env Dosyasını Düzenle

`notepad .env` ile aç ve şu değerleri düzenle:

```env
# Application
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Database (PostgreSQL)
DATABASE_URL=postgresql+asyncpg://comp_user:secure_password@localhost:5432/hissepro_comp

# Cache (Redis)
REDIS_URL=redis://localhost:6379/0

# Scheduler (şimdilik kapalı)
ENABLE_SCHEDULER=false

# Security
SECRET_KEY=dev-secret-key-change-in-production

# AI Integration (opsiyonel - şimdilik boş bırak)
# GEMINI_API_KEY=
# HONO_BASE_URL=http://localhost:8787

# CORS (Development)
ALLOWED_ORIGINS=["*"]
```

**KAYDET ve KAPAT**

---

## 🐍 3. Python Bağımlılıkları (3 dakika)

```powershell
# Sanal ortam oluştur (önerilir)
python -m venv venv

# Sanal ortamı aktif et
.\venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

**Not:** Yükleme 2-3 dakika sürebilir.

---

## 🚀 4. Uygulamayı Başlat (1 dakika)

```powershell
python main.py
```

**Başarılı başlangıç logları:**
```
INFO: 🚀 Starting HissePro Financial Analysis Engine...
INFO: ✅ Database initialized
INFO: ✅ Database and cache initialized successfully
INFO: 🎯 COMP Engine ready for pro-level financial analysis!
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Hata alıyorsan:**
- PostgreSQL çalışıyor mu? → `docker ps | findstr postgres`
- Redis çalışıyor mu? → `docker ps | findstr redis`
- `.env` dosyası doğru mu? → `type .env`

---

## ✅ 5. Test Et (3 dakika)

### Health Check

```powershell
curl http://localhost:8000/health
```

**Beklenen:**
```json
{
  "status": "healthy",
  "service": "hissepro-comp",
  "version": "2.0.0",
  "timestamp": "2026-06-27T10:50:00Z",
  "database": "connected",
  "cache": "connected"
}
```

---

### API Dokümantasyonu

Tarayıcıda aç: http://localhost:8000/docs

**Swagger UI** görmelisin:
- Interactive API documentation
- Tüm endpoint'leri test edebilirsin

---

### Root Endpoint

```powershell
curl http://localhost:8000/
```

**Beklenen:**
```json
{
  "message": "HissePro Financial Analysis Engine",
  "version": "2.0.0",
  "documentation": "/docs",
  "endpoints": {
    "companies": "/api/v1/companies/",
    "sectors": "/api/v1/sectors/",
    "admin": "/api/v1/admin/",
    "ai_context": "/api/v1/ai/"
  }
}
```

---

## 🎯 6. İlk Veri Çekimi (Manuel - Şimdilik)

**NOT:** Core servisler henüz implement edilmediği için bu adım çalışmayabilir. İmplement sonrası dene:

```powershell
# GARAN için mali tablo çek
curl -X POST http://localhost:8000/api/v1/admin/fetch `
  -H "Content-Type: application/json" `
  -d '{"tickers": ["GARAN"], "force": true}'
```

---

## 🛑 Uygulamayı Durdur

```powershell
# Ctrl+C ile uygulamayı durdur

# Docker servislerini durdur
docker stop hissepro-postgres hissepro-redis

# Docker servislerini tamamen kaldır (opsiyonel)
docker rm hissepro-postgres hissepro-redis
```

---

## 🔧 Troubleshooting

### "Database connection refused" hatası

**Çözüm:**
```powershell
# PostgreSQL çalışıyor mu?
docker ps | findstr postgres

# Çalışmıyorsa başlat
docker start hissepro-postgres

# Logları kontrol et
docker logs hissepro-postgres
```

---

### "Redis connection refused" hatası

**Çözüm:**
```powershell
# Redis çalışıyor mu?
docker ps | findstr redis

# Çalışmıyorsa başlat
docker start hissepro-redis

# Logları kontrol et
docker logs hissepro-redis
```

---

### "ModuleNotFoundError" hatası

**Çözüm:**
```powershell
# Sanal ortam aktif mi?
.\venv\Scripts\activate

# Bağımlılıkları tekrar yükle
pip install -r requirements.txt
```

---

### Port 8000 kullanımda hatası

**Çözüm 1:** Başka port kullan
```powershell
# .env dosyasında PORT değiştir
PORT=8001

# Veya komut satırından
uvicorn main:app --port 8001
```

**Çözüm 2:** Port'u işgal eden programı kapat
```powershell
# Port'u kullanan programı bul
netstat -ano | findstr :8000

# PID'yi öğren ve Task Manager'dan kapat
```

---

## 📚 Sonraki Adımlar

1. **Core Servisleri İmplement Et**
   - `COMP_ENGINE_ANALYSIS_REPORT.md` dosyasındaki Faz 2'yi takip et
   - İş Yatırım Client
   - Item Code Mapper
   - Ratio Calculator

2. **İlk Test Verisi**
   - GARAN (Bankacılık) ile başla
   - Mali tablo çek
   - Rasyoları hesapla
   - Sektör medyanı hesapla

3. **Diğer Sektörler**
   - XI_29 mapping'leri ekle
   - BIMAS, EREGL, THYAO test et
   - 14 ana sektörün hepsini kur

4. **Scheduler**
   - Otomatik veri çekme
   - 3 katmanlı schedule
   - Companies seeding

5. **Production Hazırlık**
   - Alembic migrations
   - Error handling
   - Monitoring
   - Security hardening

---

## 📞 Yardım ve Kaynaklar

### Dokümantasyon
- `README.md` - Genel overview
- `COMP_ENGINE_ANALYSIS_REPORT.md` - Detaylı analiz raporu
- `mali_tablo_sistemi_talimat.md` - Sistem tasarım dökümanı
- `hissepro_temel_analiz_ozet.md` - Metodoloji özeti

### API Dokümantasyonu
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Loglar
```powershell
# Uygulama loglarını görmek için
python main.py

# Detaylı debug logları için
# .env dosyasında DEBUG=true yap
```

---

## ✅ Checklist

- [ ] Docker Desktop kurulu ve çalışıyor
- [ ] PostgreSQL container başlatıldı
- [ ] Redis container başlatıldı
- [ ] `.env` dosyası oluşturuldu ve düzenlendi
- [ ] Python sanal ortamı oluşturuldu
- [ ] Bağımlılıklar yüklendi (`pip install -r requirements.txt`)
- [ ] Uygulama başlatıldı (`python main.py`)
- [ ] Health check başarılı (`curl http://localhost:8000/health`)
- [ ] API docs erişilebilir (`http://localhost:8000/docs`)

---

**🎉 Tebrikler! COMP Engine artık çalışıyor!**

Core servisleri implement etmek için `COMP_ENGINE_ANALYSIS_REPORT.md` dosyasındaki aksiyon planını takip edebilirsin.
