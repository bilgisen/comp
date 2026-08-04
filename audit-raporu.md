# JetBorsa Mimari Denetim Raporu

---

## Yönetici Özeti

**En kritik 3 bulgu:**

1. **KRİTİK GÜVENLİK ZAFİYETİ**: Hono AI chat, kullanıcının rolünü/tier'ını frontend'den gelen, doğrulanmamış bir body alanına (`authorization`) güveniyor. `extractUserTier()` (`ai-chat.js:20-31`) sadece prefix kontrolü yapıyor (`"proabone_"` ile başlıyor mu diye bakar). DevTools'tan `useChatStore.getState().setUserTier('proabone')` yazarak veya request body'yi değiştirerek herhangi bir kullanıcı kendini proabone yapabilir. Aynı şekilde `auth.js` middleware'deki JWT decode'u imza doğrulaması YAPMIYOR.

2. **JetToken race condition**: `chargeJT` (`jt-middleware.ts:120-207`) SELECT'i transaction DIŞINDA yapıyor, UPDATE+INSERT transaction İÇİNDE. İki eşzamanlı istek aynı `usedJt` değerini okuyup üzerine yazabilir → lost update. Ön-rezervasyon (hold) mekanizması da yok, `checkAndReserveJT` sadece bakiye kontrolü yapıyor, bloke etmiyor.

3. **Plan-Gerçek uyumsuzluğu**: Plan dokümanları Durable Object ledger, Hono'da JWT doğrulama, entity resolver gibi bileşenler varsayıyordu. Kodda: DO yok, JWT doğrulaması yok, entity resolver diye ayrı bir katman yok (ticker detection regex ile inline yapılıyor). Prompt assembly katmanlı yapı (L1-L5) kısmen var ancak planlandığı gibi değil.

---

## §1 — AUTH & KİMLİK DOĞRULAMA

### 1.1 Better Auth kurulumu nerede yaşıyor?

**Sadece TanStack frontend'de.** Hono'da Better Auth yok.

| Dosya | Açıklama |
|-------|----------|
| `tanstack/src/lib/auth.ts:13-56` | `betterAuth()` instance — Drizzle adapter, Google OAuth, session cookie, `tanstackStartCookies()` plugin |
| `tanstack/src/lib/auth-client.ts:1-5` | `createAuthClient()` — frontend React client |
| `tanstack/src/lib/auth-schema.ts:4-65` | Drizzle şeması: `user`, `session`, `account`, `verification` tabloları |
| `tanstack/src/hooks/useAuth.ts:1-95` | `useSession()` hook + credit fetch |

**Hono'da Better Auth: BULUNAMADI.** `grep "better-auth" hono/` → 0 sonuç.

### 1.2 Session/cookie yapısı

**Cookie-based.** Better Auth cookie ile çalışır:
- `auth.ts:34`: `storeStateStrategy: "cookie"`
- `auth.ts:36-40`: `session.cookieCache` enabled (5dk max age)
- `auth.ts:46-51`: `httpOnly: true`, `secure: true`, `sameSite: "lax"`
- `auth.ts:53-55`: `plugins: [tanstackStartCookies()]`

**TanStack → Hono auth akışı (ZAFİYET):**
- `chat.ts:91-96`: `mapTierToAuth()` — yerel Zustand state'ini string'e çevirir
- `chat.ts:364-365`: `"Bearer {tier}_token"` formatında sahte token üretir
- `chat.ts:377`: Bu değeri request **body**'sinde gönderir (HTTP header değil)

### 1.3 Hono tarafında kimlik doğrulama

**İki farklı mekanizma, ikisi de sorunlu:**

**3a. Auth middleware** (`hono/hono/src/middleware/auth.js:1-48`):
- `auth.js:41`: `Authorization` header'ını okur
- `auth.js:1-11`: `decodeJWTPayload()` — JWT'yi base64 decode eder, **imza doğrulamaz**
- `auth.js:13-38`: `extractRole()` — decoded payload'daki alanlara güvenir
- `main.js:87`: `app.use('/api/*', authMiddleware)` — tüm route'lara uygulanır

**3b. AI chat — bağımsız auth** (`ai-chat.js`):
- `ai-chat.js:237-238`: `const authorization = request.headers.get('Authorization') || bodyAuth || ''`
- `ai-chat.js:525`: Aynı pattern
- `ai-chat.js:20-31`: `extractUserTier()` — **sadece prefix kontrolü**, hiçbir doğrulama yok:
  ```js
  if (token.startsWith('proabone_')) return 'proabone';
  ```

### 1.4 JWT/JWKS

**JWT doğrulaması: YOK.** Kod tabanında `jose`, `jsonwebtoken`, `jwk` import'ları yok. Better Auth JWT plugin'i aktif değil (`auth.ts:53-55` sadece `tanstackStartCookies()`). `auth.js:1-11`'deki `decodeJWTPayload()` imza doğrulamaz — sadece base64 decode eder.

### 1.5 Rol/tier bilgisi nerede tutuluyor ve okunuyor?

**D1'de:**
- `auth-schema.ts:10`: `user.role` alanı (`default: "user"`)
- `schema.ts:40`: `user_credits.tier` alanı (`default: "free"`)
- `tiers.ts:3-33`: `TIER_CONFIG` — `free`, `jetabone`, `proabone`

**Hono nasıl öğreniyor:**
- TA/FA route'ları: `auth.js` middleware → JWT decode (imzasız) → `c.set('role', role)`
- AI chat: `extractUserTier()` → body'deki `authorization` alanına güveniyor

### 🔴 KRİTİK GÜVENLİK ZAFİYETİ

| Adım | Dosya:Satır | Ne oluyor? |
|------|-------------|------------|
| 1 | `chat.ts:106` | `userTier` Zustand'da client-side state |
| 2 | `chat.ts:91-96` | `mapTierToAuth()` → string mapping |
| 3 | `chat.ts:364-365` | `"Bearer {tier}_token"` üretimi |
| 4 | `chat.ts:377` | Request **body**'sinde gönderiliyor |
| 5 | `ai-chat.js:237-238` | `bodyAuth` kabul ediliyor |
| 6 | `ai-chat.js:20-31` | **Sadece prefix kontrolü, imza/doğrulama yok** |

**Herhangi bir kullanıcı kendini proabone yapabilir:**
DevTools → `useChatStore.getState().setUserTier('proabone')` veya direkt API call'da body'e `"authorization":"Bearer proabone_token"` ekleyerek.

> **Ciddiyet: YÜKSEK — Hono'ya giden her AI chat isteğinde tier atlatılabilir.**

---

## §2 — JETTOKEN / KREDİ SİSTEMİ

### 2.1 Bakiye nerede tutuluyor?

**Cloudflare D1**, `user_credits` tablosu (`schema.ts:38-51`). KV değil. Kolonlar: `userId` (PK), `tier`, `monthlyJt`, `usedJt`, `extraJt`, `polarSubId`, `polarSubStatus`, `resetAt`.

### 2.2 Decrement atomic mi?

**Hayır.** Race condition riski var:
- `jt-middleware.ts:150-154`: SELECT **transaction dışında**
- `jt-middleware.ts:158-182`: In-memory hesaplama
- `jt-middleware.ts:184-204`: Transaction sadece UPDATE+INSERT'i kapsar
- İki eşzamanlı istek aynı `usedJt` okuyup üzerine yazabilir → **lost update**
- D1'de `SELECT ... FOR UPDATE` yok

### 2.3 Model bazlı parite/oran

**Var.** `model_configs` tablosu (`schema.ts:6-22`):
- `htPer1kInput`, `htPer1kOutput` — her model için farklı JT maliyeti
- `allowedTiers` — hangi tier hangi modeli kullanabilir
- Seed data: `gemini-2.5-flash-lite` → `free`, `gemini-2.5-flash` → `jetabone/proabone`

### 2.4 Ön-rezervasyon (hold) mekanizması

**YOK.** `checkAndReserveJT` (`jt-middleware.ts:13-118`) sadece bakiye kontrolü yapar, **bloke etmez**. Gerçek düşüş sadece `chargeJT`'de, LLM yanıtı geldikten sonra yapılır.

### 2.5 Eşzamanlı istek koruması

**YOK.**
- Backend: Mutex/lock/queue mekanizması yok
- Frontend: Sadece `isLoading` flag'i (`chat.ts:193`) — aynı tab'da art arda gönderimi engeller, farklı browser/lokasyonu engellemez

---

## §3 — MEMBER / ROL MODELİ

### 3.1 Roller nerede tanımlı?

- `tiers.ts:3-33`: `TIER_CONFIG` — `free`, `jetabone`, `proabone`
- `schema.ts:40`: `user_credits.tier` — D1'de her kullanıcının aktif tier'ı
- `auth-schema.ts:10`: `user.role` — Better Auth standard role (sistem rolü, abonelik rolü değil)
- `model_configs.allowedTiers` — JSON array, hangi tier hangi modeli kullanabilir

**3 rol tanımlı:** `free` (5,000 JT/ay), `jetabone` (100,000 JT/ay), `proabone` (500,000 JT/ay)

### 3.2 Rol değişikliği (upgrade/downgrade)

**Polar.sh webhook** ile (`tanstack/src/routes/api/webhooks/polar.ts:28-131`):
- `onOrderPaid` (line 40): Tier güncellemesi
- `onSubscriptionActive` (line 65): Abonelik aktif → upsertCredits
- `onSubscriptionCanceled` (line 89): Sadece status güncellenir, tier değişmez
- `onSubscriptionRevoked` (line 105): Tier → `free`, sıfırlama

### 3.3 Rol, LLM model seçimini etkiliyor mu?

**Evet.** İki katman:
1. Frontend (`chat.ts:110-116`): `free` → üst tier geçişte model `gemini-2.5-flash-lite` → `gemini-2.5-flash` yükselir
2. Backend (`jt-middleware.ts:70-74`): `allowedTiers` kontrolü — `free` kullanıcı `gemini-2.5-flash` kullanamaz

**Hono tarafında**: Tier bilgisi prompt'a gönderilir ama önceden yaptığımız değişikliklerle (Phase 2) prompt içeriği tüm tier'lar için eşitlendi.

---

## §4 — HONO ORKESTRASYON KATMANI

### 4.1 Endpoint listesi

**Ana route'lar** (`main.js`):
| Endpoint | Method |
|----------|--------|
| `/health` | GET |
| `/api/ai/chat` | POST |
| `/api/ai/chat/stream` | POST |
| `/api/ai/ticker-search` | GET |
| `/api/sectors/industries` | GET |
| `/api/sectors/industries/:slug` | GET |
| `/api/market/symbol/:ticker/company-data` | GET |
| `/api/market/symbol/:ticker/company-profile` | GET |
| `/api/market/indices/:code` | GET |
| `/api/market/indices/:code/sector` | GET |
| `/api/market/*` | GET (catch-all proxy) |
| `/api/cron/refresh` | GET |
| `/api/cron/refresh-stocks` | GET |

**Mounted route'lar:**
- `routes/ta.js` → `/api/v1/ta/*` (7 endpoint)
- `routes/comp.js` → `/api/v1/comp/*` (25 endpoint)
- `routes/ai-report.js` → `/api/v2/ai-report/*` (3 endpoint)

**TanStack frontend route'ları:**
- `/api/ai/pre-check` (POST) — JetToken bakiye kontrol
- `/api/ai/charge` (POST) — JetToken düşüm
- `/api/webhooks/polar` (POST) — Polar.sh webhook
- `/api/models/available` (GET) — Kullanıcıya uygun modeller

### 4.2 LLM çağrısı — prompt assembly

**3 katmanlı:**

1. **Intent Router** (`intent-router.js:83`): Keyword-based intent classification → `needsTA`, `needsFA` flag'leri
2. **Data Context** (`ai-chat.js:270-363`): TA/FA/Industry/Profile verileri paralel fetch (KV cache ile)
3. **Prompt Generation** (`specialized-prompts.js:28`): Intent'e göre 7 farklı prompt builder'dan biri seçilir

**Veri çekme LLM'den ÖNCE yapılır**, ayrı faz olarak. Non-streaming'de function calling ile LLM sırasında ek veri çekilebilir (max 5 tur).

### 4.3 SSE/streaming

**Evet, implement edilmiş.** `ai-chat.js:624-680`:
- `ReadableStream` + `for await (const token of streamGemini(...))`
- SSE formatı: `data: {"type":"token","text":"..."}\n\n`
- Final: `data: {"type":"done","reply":"...","suggestions":[...]}\n\n`
- Streaming'de function calling **kapalı** (`enableFunctions: false`)

### 4.4 Veri çekme vs LLM ayrımı

**Net ayrım var.** Tüm veri çekme (TA, FA, Industry, Profile) LLM çağrısından **ÖNCE** paralel fetch edilir. Non-streaming handler'da function calling ile LLM SIRASINDA ek veri çekilebilir (lazy), streaming'de bu kapalıdır (tüm veri eager/prefetch).

---

## §5 — VERİ KATMANI D1/KV ENVANTERİ

### 5.1 D1 tabloları (var olan)

| Tablo | Dosya | Not |
|-------|-------|-----|
| `user` | `auth-schema.ts:4` | Better Auth |
| `session` | `auth-schema.ts:15` | Better Auth |
| `account` | `auth-schema.ts:32` | Better Auth |
| `verification` | `auth-schema.ts:54` | Better Auth |
| `model_configs` | `schema.ts:6` | JetToken model oranları |
| `tariff_history` | `schema.ts:24` | Tarife değişiklik log'u |
| `user_credits` | `schema.ts:38` | JetToken bakiyeleri |
| `usage_logs` | `schema.ts:53` | Kullanım log'ları |
| `chat_sessions` | `schema.ts:70` | Chat oturumları |
| `chat_messages` | `schema.ts:84` | Chat mesajları |
| `webhook_events` | `schema.ts:100` | Webhook işleme takibi |

**Not:** `mali_tablo_sistemi_talimat.md`'deki finansal tablo şeması **D1'de yok**. Finansal veriler Finveri API üzerinden çekiliyor, D1'de depolanmıyor.

### 5.2 KV key pattern'leri

**En kritik KV anahtarları** (`hono/hono/src/`):

| Key pattern | TTL | Kullanım yeri |
|-------------|-----|---------------|
| `ta:{ticker}:{tier}` | 300s | `ai-chat.js:94` |
| `fa:{ticker}:{tier}` | 300s | `ai-chat.js:112` |
| `profile:{ticker}` | 86400s | `ai-chat.js:130` |
| `index:{code}` | 900s | `main.js:295` |
| `pool:bist_stocks:data` | 300s | `main.js:358` |
| `pool:market_summary:data` | 300s | `main.js:384` |
| `symbol:{ticker}` | 120s | `main.js:628` |
| `company-profile:{ticker}` | 86400s | `cache.js:129` |
| `tickers:data` | 60-300s | `tanstack/tickers.ts:39` |

### 5.3 Durable Object

**YOK.** Tüm projelerde (tanstack, hono, finveri, comp/temel) Durable Object binding tanımlı değil. `wrangler.jsonc` dosyalarında DO yok.

---

## §6 — PLAN vs GERÇEK KARŞILAŞTIRMA TABLOSU

> Plan dokümanları dosya olarak kod tabanında bulunamadı. Karşılaştırma, Claude'un talimatındaki plan varsayımlarına göre yapılmıştır.

| Bileşen | Planda Varsayılan | Kodda Gerçek Durum | Fark/Risk |
|---------|-------------------|-------------------|-----------|
| **Auth (JWT/JWKS)** | Hono'da JWKS ile stateless doğrulama | `auth.js:1-11` base64 decode yapar, **imza doğrulamaz**. AI chat ise body'deki düz metne güvenir | **KRİTİK RİSK** — JWT doğrulaması yok, tier atlatılabilir |
| **Session/cookie akışı** | — | Better Auth cookie-based. TanStack'ten Hono'ya **resmi bir auth akışı yok** — chat body'sinde `authorization` alanı gönderilir | **KRİTİK RİSK** — Backend kullanıcıyı bağımsız doğrulamıyor |
| **JetToken ledger** | Durable Object, atomic decrement | D1'de `user_credits` tablosu. SELECT transaction dışında, lost update riski var | **ORTA RİSK** — DO yok, race condition açık |
| **Model parite tablosu** | `model_catalog` DB'de, oranlı | `model_configs` tablosu (`schema.ts:6`), `htPer1kInput`/`htPer1kOutput` oranlı. `allowedTiers` ile tier kontrolü | **UYUMLU** |
| **Rol enforcement** | Backend'de doğrulanır | TA route'lar: imzasız JWT decode. AI chat: **hiç doğrulama yok** | **KRİTİK RİSK** — DevTools ile bypass |
| **Entity resolver** | Deterministik lookup, LLM'den önce | Ayrı bir `entity-resolver` katmanı **yok**. Ticker detection `ai-chat.js:249-267`'de inline regex ile yapılır | **ORTA FARK** — Planlanan gibi değil, inline çözüm |
| **Prompt assembly (L1-L5)** | Katmanlı, D1'den entity verisi enjekte | 3 katmanlı: Intent Router → Data Context → Prompt Builder. Veri LLM'den önce çekilir. Katman sayısı plandakinden az | **KISMEN UYUMLU** — Temel yapı var ama planlanan kadar sofistike değil |
| **SSE streaming** | Var, AppShell seviyesinde kalıcı | `ai-chat.js:624-680`'de `ReadableStream` ile implement edilmiş. Kalıcı değil, her istek için yeni stream | **UYUMLU** |
| **D1 şeması (mali tablo)** | Tam şema, mali_tablo dokümanı | Finansal tablolar D1'de **yok**. Finveri API üzerinden canlı çekilir | **BÜYÜK FARK** — Plan D1'de finansal veri depolama öngörmüştü |
| **Function calling** | — | `callGemini`'de açık (5 tur), `streamGemini`'de kapalı. `get_technical_indicators`, `get_fundamental_ratios` vb. fonksiyonlar tanımlı | — |
| **Prompt caching** | — | KV caching: TA 300s, FA 300s, Profile 86400s. LLM response cache yok | — |

---

## Açık Sorular (kodda bulunamayan / kullanıcıya sorulması gerekenler)

1. **Polar.sh webhook güvenliği**: Webhook secret doğrulaması var mı kodda? Polar'dan gelen isteğin gerçekten Polar'dan geldiğini nasıl anlıyor? (`polar.ts` dosyasına bakıldı, secret doğrulaması görülmedi)
2. **`user.role` vs `user_credits.tier` farkı**: Better Auth'un `user.role` alanı (`default: "user"`) ile `user_credits.tier` (`default: "free"`) arasında senkronizasyon var mı? Yoksa iki ayrı rol mü var?
3. **Free tier kullanıcıları nasıl oluşuyor?** Yeni kayıt olan kullanıcıya `user_credits` satırı otomatik ekleniyor mu (JT middleware auto-provision yapıyor), yoksa bir migration/setup adımı mı gerekiyor?
4. **Hata durumunda Polar webhook retry mekanizması**: Webhook işlenirken hata olursa (örn. D1 down), Polar yeniden dener mi? Kodda idempotency (event_id kontrolü) var mı? (`webhook_events` tablosu var ama `schema.ts:100-105` — kullanılıyor mu?)
5. **Mali tabloların kaynağı**: Finansal veriler D1'de değil Finveri API'den geliyor. Bu bilinçli bir karar mı, yoksa plandaki gibi D1'e taşınması mı gerekiyor?

---

*Rapor tarihi: 28 Temmuz 2026*
*Raporu hazırlayan: opencode (deepseek-v4-flash-free)*
