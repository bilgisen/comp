# Temel - Cloudflare Python Worker Setup

## Prerequisites

- Node.js + npm (for wrangler)
- Cloudflare account with D1 and KV enabled
- Python Workers beta enabled on Cloudflare

## Installation

```bash
# 1. Login to Cloudflare
npx wrangler login

# 2. Create D1 database
npx wrangler d1 create temel-db

# 3. Create KV namespace
npx wrangler kv:namespace create "TEMEL_CACHE"

# 4. Update wrangler.toml with the IDs from steps 2-3

# 5. Apply schema
npx wrangler d1 execute temel-db --file=src/db/schema.sql

# 6. Seed companies
npx wrangler d1 execute temel-db --file=src/db/seed_companies.sql

# 7. Seed item code mappings
npx wrangler d1 execute temel-db --file=src/db/seed_item_codes.sql

# 8. Start dev server
npx wrangler dev

# 9. Deploy
npx wrangler deploy
```

## Project Structure

```
temel/
├── wrangler.toml              # Worker configuration
├── SETUP.md                   # This file
├── src/
│   ├── index.py               # Worker entry point (fetch handler)
│   ├── config.py              # Environment settings
│   ├── db/
│   │   ├── client.py          # D1 helper
│   │   ├── schema.sql         # Table definitions
│   │   ├── seed_companies.sql # Company data seed
│   │   └── seed_item_codes.sql # Item code mappings
│   ├── kv/
│   │   └── cache.py           # KV cache wrapper
│   ├── models/
│   │   ├── company.py         # Company CRUD
│   │   ├── financial.py       # Financial statements & ratios
│   │   └── metrics.py         # Market metrics
│   ├── services/
│   │   ├── isyatirim.py       # Is Yatirim API client
│   │   ├── ratio_calculator.py # Ratio calculation engine
│   │   └── ai_context.py      # AI context builder
│   └── routers/
│       ├── health.py          # Health check endpoints
│       ├── companies.py       # Company API routes
│       └── analysis.py        # AI analysis routes
├── scripts/
│   └── seed_from_excel.py     # Excel import script
└── tests/
```

## Environment Variables (wrangler.toml [vars])

| Variable | Default | Description |
|----------|---------|-------------|
| ISYATIRIM_BASE_URL | https://www.isyatirim.com.tr | Is Yatirim API base |
| ISYATIRIM_TIMEOUT | 30 | Request timeout (s) |
| ISYATIRIM_RATE_LIMIT | 20 | Requests per minute |
| ISYATIRIM_DELAY | 3.0 | Delay between requests |
| CACHE_TTL_RATIOS | 3600 | Ratio cache TTL (s) |
| CACHE_TTL_COMPANY | 21600 | Company cache TTL (s) |
| CACHE_TTL_AI_CONTEXT | 1800 | AI context cache TTL (s) |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | / | API info |
| GET | /api/v1/sectors | List sectors |
| GET | /api/v1/companies | List companies |
| GET | /api/v1/companies/search?q= | Search companies |
| GET | /api/v1/companies/{ticker} | Company profile |
| GET | /api/v1/companies/{ticker}/statements | Financial statements |
| GET | /api/v1/companies/{ticker}/ratios | Calculated ratios |
| GET | /api/v1/companies/{ticker}/trends | Ratio trends |
| GET | /api/v1/companies/{ticker}/calculate | Trigger calculation |
| GET | /api/v1/ai/context/{ticker} | AI chatbot context |
| GET | /api/v1/ai/analysis/{ticker} | Temel analysis |
| GET | /api/v1/ai/swot/{ticker} | SWOT analysis |
| GET | /api/v1/ai/fundamental-report/{ticker} | Full report |
