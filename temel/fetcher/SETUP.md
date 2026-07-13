# Temel Fetcher - Scheduled Data Fetch Worker

Fetches financial data from Is Yatirim API on a schedule.

## Setup

```bash
# Deploy fetcher worker
cd fetcher
npx wrangler deploy

# The cron triggers are: 05:00 and 17:00 daily (TR timezone)
# You can also trigger manually:
# npx wrangler d1 execute temel-db --command="..."
```

## Cron Schedule

- `0 5 * * *` - 05:00 UTC (08:00 TR) - Morning fetch
- `0 17 * * *` - 17:00 UTC (20:00 TR) - Evening fetch

## Manual Trigger

```bash
curl -X POST https://temel-fetcher.workers.dev/
```
