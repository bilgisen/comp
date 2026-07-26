import json
import math
from datetime import datetime, timezone
from urllib.parse import unquote, urlparse, parse_qs
from workers import WorkerEntrypoint, Response

# ─── Pure-Python Statistics (No NumPy/SciPy) ────────────────────────────────

def _djb2_hash(s):
    h = 5381
    for c in s:
        h = ((h << 5) + h) + ord(c)
        h = h & 0xFFFFFFFF
    return format(h, '08x')

# ─── KV Cache Helper ────────────────────────────────────────────────────────

CACHE_TTL = 3600  # 1 hour default

def _cache_key(path, q):
    raw = json.dumps({"p": path, "q": q}, sort_keys=True)
    return "sw:" + _djb2_hash(raw)

def _compute_etag(data):
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False)
    h = 5381
    for c in raw:
        h = ((h << 5) + h) + ord(c)
        h = h & 0xFFFFFFFF
    return format(h, '08x')

async def _cache_get(kv, key):
    if kv is None: return None
    val = await kv.get(key)
    if not val: return None
    try:
        entry = json.loads(val)
        # Support both old (bare dict) and new ({data, etag}) format
        if isinstance(entry, dict) and "data" in entry and "etag" in entry:
            return entry
        return {"data": entry, "etag": _compute_etag(entry)}
    except:
        return None

async def _cache_set(kv, key, data, etag=None, ttl=CACHE_TTL):
    if kv is None: return
    if etag is None:
        etag = _compute_etag(data)
    entry = json.dumps({"data": data, "etag": etag, "ts": datetime.now(timezone.utc).isoformat()})
    await kv.put(key, entry, expiration_ttl=ttl)

def _log(msg, extra=None):
    payload = {"msg": msg, "ts": datetime.now(timezone.utc).isoformat()}
    if extra: payload["extra"] = extra
    print(json.dumps(payload))

async def _cached_json(kv, key, data, status=200):
    etag = _compute_etag(data)
    if kv is not None and key:
        await _cache_set(kv, key, data, etag)
    headers = {"ETag": etag}
    if key:
        headers["X-Cache"] = "MISS"
        headers["X-Cache-Key"] = key
    return Response.json(data, status=status, headers=headers)

def _median(values):
    arr = sorted(values)
    n = len(arr)
    if n == 0: return 0.0
    if n % 2 == 1: return float(arr[n // 2])
    return (arr[n // 2 - 1] + arr[n // 2]) / 2.0

def _percentile(values, q):
    arr = sorted(values)
    n = len(arr)
    if n == 0: return 0.0
    k = (q / 100.0) * (n - 1)
    f = int(math.floor(k))
    c = int(math.ceil(k))
    if f >= n: return float(arr[-1])
    if f == c or f >= n: return float(arr[f])
    return arr[f] * (c - k) + arr[c] * (k - f)

def _robust_std(values):
    p25 = _percentile(values, 25)
    p75 = _percentile(values, 75)
    iqr = p75 - p25
    if iqr < 1e-10: return 0.0
    return iqr / 1.349

def _winsorize(values, lo_pct=5.0, hi_pct=95.0):
    if len(values) < 5: return values[:]
    lo = _percentile(values, lo_pct)
    hi = _percentile(values, hi_pct)
    return [max(lo, min(v, hi)) for v in values]

def _weighted_quantile(values, weights, q):
    if not values or not weights: return 0.0
    paired = list(zip(values, [max(w, 0.01) for w in weights]))
    paired.sort(key=lambda x: x[0])
    sorted_vals = [p[0] for p in paired]
    sorted_wts = [p[1] for p in paired]
    total = sum(sorted_wts)
    target = q * total
    cum = 0.0
    for i in range(len(sorted_vals)):
        cum += sorted_wts[i]
        if cum >= target:
            return float(sorted_vals[i])
    return float(sorted_vals[-1])

def _safe_div(a, b):
    if a is None or b is None: return None
    try: return a / b if abs(b) > 1e-12 else None
    except: return None

# ─── Sector Consolidation: 54 raw sectors -> 14 groups ───────────────────────

SECTOR_CONSOLIDATION = {
    "Bankacılık": "Bankacilik_Finans",
    "Yatırım Ortaklıkları": "Bankacilik_Finans",
    "Aracı Kurumlar": "Bankacilik_Finans",
    "Fin.Kiralama ve Faktoring": "Bankacilik_Finans",
    "Varlık Yönetim": "Bankacilik_Finans",
    "Sigorta": "Sigortacilik",
    "GYO": "GYO",
    "Elektrik Üretim": "Enerji_Altyapi",
    "Elektrik - Doğalgaz Dağıtım": "Enerji_Altyapi",
    "Elektrik Enerji Ürt.Teçh/Tesis Kurulum": "Enerji_Altyapi",
    "Petrol": "Enerji_Altyapi",
    "Demir-Çelik Temel": "Sanayi_Metal_Kimya",
    "Demir-Çelik Döküm": "Sanayi_Metal_Kimya",
    "Kimyasal Ürün": "Sanayi_Metal_Kimya",
    "Çimento": "Sanayi_Metal_Kimya",
    "Seramik": "Sanayi_Metal_Kimya",
    "Cam": "Sanayi_Metal_Kimya",
    "Boya": "Sanayi_Metal_Kimya",
    "Kablo": "Sanayi_Metal_Kimya",
    "Endüstriyel Makine -Teçhizat Üretim": "Sanayi_Metal_Kimya",
    "İnşaat Malzemeleri": "Insaat_Yapi",
    "İnşaat- Taahhüt": "Insaat_Yapi",
    "Otomotiv": "Otomotiv_Savunma_Makine",
    "Otomotiv Parçası": "Otomotiv_Savunma_Makine",
    "Otomotiv Lastiği": "Otomotiv_Savunma_Makine",
    "Savunma": "Otomotiv_Savunma_Makine",
    "Sağlık ve İlaç": "Saglik_Ilac",
    "Teknoloji": "Teknoloji_Iletisim",
    "Bilgisayar Toptancılığı": "Teknoloji_Iletisim",
    "İletişim": "Teknoloji_Iletisim",
    "İletişim Cihazları": "Teknoloji_Iletisim",
    "Gıda": "Gida_Icecek_Tarim",
    "Meşrubat / İçecek": "Gida_Icecek_Tarim",
    "Hayvancılık": "Gida_Icecek_Tarim",
    "Tarım Kimyasalları": "Gida_Icecek_Tarim",
    "Tekstil Entegre": "Tuketim_Perakende_Tekstil",
    "Endüstriyel Tekstil": "Tuketim_Perakende_Tekstil",
    "Deri Giyim": "Tuketim_Perakende_Tekstil",
    "Kağıt Ürünleri": "Tuketim_Perakende_Tekstil",
    "Mobilya": "Tuketim_Perakende_Tekstil",
    "Kırtasiye": "Tuketim_Perakende_Tekstil",
    "Perakande - Ticaret": "Tuketim_Perakende_Tekstil",
    "Pazarlama": "Tuketim_Perakende_Tekstil",
    "Dayanıklı Tüketim": "Tuketim_Perakende_Tekstil",
    "Ulaştırma-Lojistik": "Ulastirma_Lojistik",
    "Havayolları ve Hizm.": "Ulastirma_Lojistik",
    "Turizm": "Turizm_Medya_Eglence",
    "Medya": "Turizm_Medya_Eglence",
    "Eğlence Hizmetleri": "Turizm_Medya_Eglence",
    "Holdingler": "Holdingler",
    "Madencilik": "Holdingler",
    "Diğer": None,
    "Spor": None,
}

SECTOR_GROUP_NAMES = {
    "Bankacilik_Finans": "Bankacılık & Finans",
    "Sigortacilik": "Sigortacılık", "GYO": "GYO",
    "Enerji_Altyapi": "Enerji & Altyapı",
    "Sanayi_Metal_Kimya": "Sanayi & Metal & Kimya",
    "Insaat_Yapi": "İnşaat & Yapı Malzemeleri",
    "Otomotiv_Savunma_Makine": "Otomotiv & Savunma & Makine",
    "Saglik_Ilac": "Sağlık & İlaç",
    "Teknoloji_Iletisim": "Teknoloji & İletişim",
    "Gida_Icecek_Tarim": "Gıda & İçecek & Tarım",
    "Tuketim_Perakende_Tekstil": "Tüketim & Perakende & Tekstil",
    "Ulastirma_Lojistik": "Ulaştırma & Lojistik",
    "Turizm_Medya_Eglence": "Turizm & Medya & Eğlence",
    "Holdingler": "Holdingler",
}

# ─── Economic Bounds (F3 filter) ────────────────────────────────────────────

ECONOMIC_BOUNDS = {
    "_default": {
        "pe": (0.0, 150.0), "pb": (0.0, 20.0), "ev_ebitda": (0.0, 60.0), "ev_sales": (0.0, 30.0),
        "current_ratio": (0.1, 15.0), "cash_ratio": (0.0, 10.0),
        "debt_equity": (-2.0, 25.0), "interest_coverage": (-20.0, 50.0),
        "gross_margin": (-0.50, 0.95), "net_margin": (-2.0, 0.60), "roe": (-1.0, 1.5), "roa": (-0.3, 0.4),
        "eps": (-500.0, 5000.0), "book_per_share": (-50.0, 5000.0), "profit_growth": (-10.0, 20.0),
        "inventory_turnover": (0.0, 10000.0),
    },
    "Bankacilik_Finans": {
        "pe": (0.0, 25.0), "pb": (0.0, 5.0), "roe": (-0.3, 0.5), "roa": (-0.05, 0.08), "net_margin": (-0.5, 0.5),
    },
    "Sigortacilik": {
        "pe": (0.0, 30.0), "pb": (0.0, 5.0), "roe": (-0.3, 0.8), "roa": (-0.05, 0.08), "net_margin": (-0.3, 0.5),
    },
    "GYO": {
        "pe": (0.0, 50.0), "pb": (0.0, 5.0), "roe": (-0.3, 0.5), "net_margin": (-0.5, 0.6), "debt_equity": (0.0, 20.0),
    },
    "Enerji_Altyapi": {
        "pe": (0.0, 80.0), "pb": (0.0, 15.0), "ev_ebitda": (0.0, 25.0), "debt_equity": (-1.0, 20.0),
        "current_ratio": (0.1, 10.0), "net_margin": (-1.0, 0.6),
    },
    "Teknoloji_Iletisim": {
        "pe": (0.0, 200.0), "pb": (0.0, 30.0), "gross_margin": (-0.1, 0.99), "net_margin": (-5.0, 0.7),
    },
}

# ─── Pillar Configuration (3 pillars) ───────────────────────────────────────

PILLAR_CONFIG = {
    "_default": {
        "finansal_saglik": {"weight": 0.40, "min_ratios": 2, "ratios": {
            "current_ratio": 0.30, "cash_ratio": 0.15, "debt_equity": 0.35, "interest_coverage": 0.20,
        }},
        "karlilik_buyume": {"weight": 0.35, "min_ratios": 2, "ratios": {
            "roe": 0.30, "roa": 0.15, "net_margin": 0.25, "gross_margin": 0.15, "profit_growth": 0.15,
        }},
        "degerleme": {"weight": 0.25, "min_ratios": 1, "ratios": {
            "pe": 0.35, "pb": 0.25, "ev_ebitda": 0.25, "ev_sales": 0.15,
        }},
    },
    "Bankacilik_Finans": {
        "finansal_saglik": {"weight": 0.35, "min_ratios": 1, "ratios": {
            "roe": 1.0,
        }},
        "karlilik_buyume": {"weight": 0.45, "min_ratios": 1, "ratios": {
            "roe": 0.40, "net_margin": 0.35, "profit_growth": 0.25,
        }},
        "degerleme": {"weight": 0.20, "min_ratios": 1, "ratios": {
            "pe": 0.50, "pb": 0.50,
        }},
    },
    "Sigortacilik": {
        "finansal_saglik": {"weight": 0.35, "min_ratios": 1, "ratios": {
            "roe": 1.0,
        }},
        "karlilik_buyume": {"weight": 0.40, "min_ratios": 1, "ratios": {
            "roe": 0.40, "net_margin": 0.35, "profit_growth": 0.25,
        }},
        "degerleme": {"weight": 0.25, "min_ratios": 1, "ratios": {
            "pe": 0.50, "pb": 0.50,
        }},
    },
    "GYO": {
        "finansal_saglik": {"weight": 0.30, "min_ratios": 1, "ratios": {
            "roe": 0.60, "profit_growth": 0.40,
        }},
        "karlilik_buyume": {"weight": 0.35, "min_ratios": 1, "ratios": {
            "roe": 0.50, "net_margin": 0.30, "profit_growth": 0.20,
        }},
        "degerleme": {"weight": 0.35, "min_ratios": 1, "ratios": {
            "pe": 0.50, "pb": 0.50,
        }},
    },
    "Teknoloji_Iletisim": {
        "finansal_saglik": {"weight": 0.25, "min_ratios": 1, "ratios": {
            "current_ratio": 0.40, "cash_ratio": 0.20, "debt_equity": 0.40,
        }},
        "karlilik_buyume": {"weight": 0.50, "min_ratios": 2, "ratios": {
            "roe": 0.25, "roa": 0.15, "net_margin": 0.25, "gross_margin": 0.15, "profit_growth": 0.20,
        }},
        "degerleme": {"weight": 0.25, "min_ratios": 1, "ratios": {
            "pe": 0.50, "pb": 0.30, "ev_sales": 0.20,
        }},
    },
    "Holdingler": {
        "finansal_saglik": {"weight": 0.35, "min_ratios": 1, "ratios": {
            "debt_equity": 0.50, "current_ratio": 0.25, "interest_coverage": 0.25,
        }},
        "karlilik_buyume": {"weight": 0.40, "min_ratios": 1, "ratios": {
            "roe": 0.40, "net_margin": 0.30, "roa": 0.15, "profit_growth": 0.15,
        }},
        "degerleme": {"weight": 0.25, "min_ratios": 1, "ratios": {
            "pe": 0.40, "pb": 0.25, "ev_ebitda": 0.20, "ev_sales": 0.15,
        }},
    },
}

HIGHER_IS_BETTER = {
    "current_ratio": True, "cash_ratio": True, "debt_equity": False, "interest_coverage": True,
    "roe": True, "roa": True, "net_margin": True, "gross_margin": True, "profit_growth": True,
    "pe": False, "pb": False, "ev_ebitda": False, "ev_sales": False,
    "eps": True, "book_per_share": True, "inventory_turnover": True,
}

# ─── Absolute Score Thresholds ──────────────────────────────────────────────

ABSOLUTE_THRESHOLDS = {
    "current_ratio": [(0.5, 0), (0.8, 25), (1.2, 50), (1.8, 75), (float("inf"), 100)],
    "cash_ratio": [(0.05, 0), (0.15, 25), (0.30, 50), (0.50, 75), (float("inf"), 100)],
    "debt_equity": [(0.0, 100), (1.0, 75), (2.5, 50), (4.0, 25), (float("inf"), 0)],
    "interest_coverage": [(0.0, 0), (1.0, 25), (3.0, 50), (6.0, 75), (float("inf"), 100)],
    "roe": [(0.0, 0), (0.05, 25), (0.10, 50), (0.18, 75), (float("inf"), 100)],
    "roa": [(-0.05, 0), (0.0, 25), (0.05, 50), (0.10, 75), (float("inf"), 100)],
    "net_margin": [(-0.10, 0), (0.0, 25), (0.05, 50), (0.12, 75), (float("inf"), 100)],
    "gross_margin": [(0.0, 0), (0.10, 25), (0.20, 50), (0.35, 75), (float("inf"), 100)],
    "profit_growth": [(-0.50, 0), (-0.10, 25), (0.0, 50), (0.20, 75), (float("inf"), 100)],
    "pe": [(0.0, 100), (8.0, 75), (15.0, 50), (25.0, 25), (float("inf"), 0)],
    "pb": [(0.0, 100), (1.0, 75), (3.0, 50), (7.0, 25), (float("inf"), 0)],
}

ABSOLUTE_LABELS = [
    (80, "GUCLU"), (60, "SAGLIKLI"), (40, "ORTA"), (20, "ZAYIF"), (0, "KRITIK"),
]

# ─── Helpers ────────────────────────────────────────────────────────────────

def _get_consolidated(sector_main):
    return SECTOR_CONSOLIDATION.get(sector_main)

def _get_pillar_config(sector_main):
    c = _get_consolidated(sector_main)
    return PILLAR_CONFIG.get(c, PILLAR_CONFIG["_default"])

def _get_bounds(sector_main):
    c = _get_consolidated(sector_main)
    return ECONOMIC_BOUNDS.get(c, ECONOMIC_BOUNDS["_default"])

def _f3_economic_validity(ratio_code, value, sector_main):
    bounds = _get_bounds(sector_main)
    default_bounds = ECONOMIC_BOUNDS["_default"]
    b = bounds.get(ratio_code) or default_bounds.get(ratio_code)
    if b is None: return False
    lo, hi = b
    if lo is not None and value < lo: return False
    if hi is not None and value > hi: return False
    return True

def _assess_reliability(n):
    if n >= 10: return "HIGH"
    if n >= 5: return "MEDIUM"
    if n >= 3: return "LOW"
    return "INSUFFICIENT"

def _sigmoid_score(value, peer_values, higher_is_better=True, steepness=0.8):
    valid = [v for v in peer_values if v is not None and math.isfinite(v)]
    if len(valid) < 3: return None, None
    median = _median(valid)
    robust_std = _robust_std(valid)
    if robust_std < 1e-10: return 50.0, median
    z = (value - median) / robust_std
    if not higher_is_better: z = -z
    try:
        score = 100.0 / (1.0 + math.exp(-steepness * z))
    except OverflowError:
        score = 99.99 if z > 0 else 0.01
    score = max(0.01, min(99.99, score))
    return score, median

def _reliability_dampening(raw_score, reliability):
    factors = {"HIGH": 1.0, "MEDIUM": 0.80, "LOW": 0.55}
    factor = factors.get(reliability)
    if factor is None: return None
    return 50.0 + (raw_score - 50.0) * factor

def _absolute_ratio_score(value, thresholds):
    if value is None: return None
    for max_val, score in thresholds:
        if value <= max_val:
            return score
    return 50.0

# ─── Worker ─────────────────────────────────────────────────────────────────

class Default(WorkerEntrypoint):

    async def fetch(self, request):
        try:
            return await self._fetch_impl(request)
        except Exception as e:
            _log("fetch_error", {"error": str(e)[:500]})
            return Response.json({"error": str(e)}, status=500)

    async def _fetch_impl(self, request):
        url_str = str(request.url)
        parsed = urlparse(url_str)
        path = unquote(parsed.path).rstrip("/")
        if not path: path = "/"
        q = {}
        if parsed.query:
            for part in parsed.query.split("&"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    q[k] = v

        _log("fetch", {"path": path, "method": request.method})

        # KV cache for GET endpoints (skip compute/seed mutations)
        try:
            kv = self.env.TEMEL_CACHE
        except AttributeError:
            kv = None
        use_cache = request.method == "GET" and path not in ("/benchmarks/compute", "/scores/compute", "/seed_consolidation")
        client_etag = (request.headers.get("If-None-Match") or "").strip('"')

        ck = None
        if use_cache:
            ck = _cache_key(path, q)
            cached = await _cache_get(kv, ck)
            if cached:
                stored_etag = cached.get("etag", "")
                # ETag match → 304 Not Modified
                if client_etag and stored_etag and client_etag == stored_etag:
                    _log("cache_304", {"path": path})
                    return Response(None, status=304, headers={"ETag": stored_etag, "X-Cache": "HIT", "X-Cache-Key": ck})
                # Cache hit → serve cached data
                _log("cache_hit", {"path": path})
                return Response.json(cached["data"], headers={"ETag": stored_etag, "X-Cache": "HIT", "X-Cache-Key": ck})

        resp = await self._route(request, path, q, kv, ck if use_cache else None)
        return resp

    async def _route(self, request, path, q, kv, cache_key):
        _log("route", {"path": path})
        if path == "/benchmarks/compute":
            return await self._compute_benchmarks(q)
        if path == "/scores/compute":
            return await self._compute_scores(q)
        if path == "/seed_consolidation":
            return await self._seed_consolidation()
        if path.startswith("/score/"):
            return await self._get_score(path[len("/score/"):], q, kv, cache_key)
        if path.startswith("/absolute/"):
            return await self._get_absolute(path[len("/absolute/"):], kv, cache_key)
        if path.startswith("/rankings/"):
            return await self._get_rankings(path[len("/rankings/"):], q, kv, cache_key)
        if path.startswith("/compare/"):
            return await self._compare(path[len("/compare/"):], kv, cache_key)
        if path == "/sectors":
            return await self._list_sectors(kv, cache_key)
        if path.startswith("/sectors/"):
            return await self._sector_detail(path[len("/sectors/"):], q, kv, cache_key)

        return Response.json({"error": "not found"}, status=404)

    async def scheduled(self, event):
        _log("cron_start", {"type": event.type if hasattr(event, 'type') else 'scheduled'})
        await self._compute_benchmarks({})
        cursor = 0
        while True:
            r = await self._compute_scores({"cursor": str(cursor)})
            if r.get("cursor") == 0:
                break
            cursor = r["cursor"]
        _log("cron_done", {})

    async def _seed_consolidation(self):
        db = self.env.TEMEL_DB
        count = 0
        for raw, cons in SECTOR_CONSOLIDATION.items():
            is_spor = 1 if raw == "Spor" else 0
            r = await db.prepare(
                "INSERT OR IGNORE INTO sector_consolidation (sector_raw, sector_group, sector_consolidated, is_spor) VALUES (?, ?, ?, ?)"
            ).bind(raw, None, cons, is_spor).run()
            if r.success: count += 1
        return Response.json({"seeded": count, "total": len(SECTOR_CONSOLIDATION)})

    # ─── Benchmark Computation ─────────────────────────────────────────

    async def _compute_benchmarks(self, params):
        db = self.env.TEMEL_DB
        sector_name = params.get("sector")
        _log("compute_benchmarks_start", {"sector": sector_name or "all"})

        if sector_name:
            sectors = [sector_name]
        else:
            r = await db.prepare("SELECT DISTINCT sector_main FROM companies WHERE is_active = 1 ORDER BY sector_main").all()
            sectors = [row["sector_main"] for row in r.results]

        period_key = "TTM"
        all_results = []

        for sec in sectors:
            consolidated = _get_consolidated(sec)
            types_list = ["sector"]
            if consolidated:
                types_list.append("group")

            for btype in types_list:
                name = sec if btype == "sector" else consolidated
                result = await self._compute_single_benchmark(db, name, btype, period_key, sec)
                if result:
                    all_results.append(result)

        mr = await self._compute_market_benchmarks(db, period_key)
        if mr:
            all_results.extend(mr)

        _log("compute_benchmarks_done", {"benchmarks_count": len(all_results), "sectors_count": len(sectors)})
        return Response.json({"benchmarks_computed": len(all_results), "sectors": len(sectors)})

    async def _compute_single_benchmark(self, db, name, btype, period_key, sector_main_for_bounds):
        if btype == "sector":
            r = await db.prepare("SELECT ticker, market_cap FROM companies WHERE sector_main = ? AND is_active = 1").bind(name).all()
        elif btype == "group":
            r = await db.prepare(
                "SELECT c.ticker, c.market_cap FROM companies c JOIN sector_consolidation sc ON c.sector_main = sc.sector_raw WHERE sc.sector_consolidated = ? AND c.is_active = 1"
            ).bind(name).all()
        else:
            return None

        rows = [dict(x) for x in r.results]
        tickers = [x["ticker"] for x in rows]
        mcaps = {x["ticker"]: (x["market_cap"] or 0) for x in rows}
        if len(tickers) < 3: return None

        placeholders = ",".join("?" for _ in tickers)
        r2 = await db.prepare(
            f"SELECT ticker, ratio_code, ratio_value FROM company_ratios WHERE ticker IN ({placeholders}) AND period_key = ? AND ratio_value IS NOT NULL AND calculation_method = 'v2'"
        ).bind(*tickers, period_key).all()

        ratio_map = {}
        for row in r2.results:
            t = row["ticker"]
            rc = row["ratio_code"]
            val = row["ratio_value"]
            if val is not None and math.isfinite(val):
                ratio_map.setdefault(rc, []).append((t, val))

        results = []
        for ratio_code in HIGHER_IS_BETTER:
            raw = ratio_map.get(ratio_code, [])
            if len(raw) < 3: continue
            filtered = []
            for t, val in raw:
                if val is None or not math.isfinite(val): continue
                if not _f3_economic_validity(ratio_code, val, sector_main_for_bounds): continue
                filtered.append({"ticker": t, "value": val, "market_cap": mcaps.get(t, 0)})
            if len(filtered) < 3: continue
            vals = [p["value"] for p in filtered]
            if len(vals) >= 5:
                wvals = _winsorize(vals, 5, 95)
                for i, p in enumerate(filtered):
                    p["value"] = wvals[i]
            n = len(filtered)
            reliability = _assess_reliability(n)
            clean_vals = [p["value"] for p in filtered]
            mc_wts = [max(p["market_cap"], 0.01) for p in filtered]
            median_ew = _median(clean_vals)
            median_mc = _weighted_quantile(clean_vals, mc_wts, 0.5)
            p25 = _percentile(clean_vals, 25)
            p75 = _percentile(clean_vals, 75)
            now = datetime.now(timezone.utc).isoformat()
            await db.prepare(
                "INSERT OR REPLACE INTO sector_benchmarks (sector_name, benchmark_type, ratio_code, period_key, median_ew, median_mc, p25, p75, n_peers, reliability, computed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            ).bind(name, btype, ratio_code, period_key, median_ew, median_mc, p25, p75, n, reliability, now).run()
            results.append({"ratio": ratio_code, "n": n, "reliability": reliability})

        return {"sector": name, "type": btype, "ratios": len(results)} if results else None

    async def _compute_market_benchmarks(self, db, period_key):
        results = []
        for rc in ["pe", "pb", "ev_ebitda", "ev_sales"]:
            r = await db.prepare(
                "SELECT cr.ticker, cr.ratio_value, c.market_cap FROM company_ratios cr JOIN companies c ON cr.ticker = c.ticker WHERE cr.ratio_code = ? AND cr.period_key = ? AND cr.ratio_value IS NOT NULL AND cr.ratio_value > 0 AND cr.calculation_method = 'v2'"
            ).bind(rc, period_key).all()
            rows = [dict(x) for x in r.results]
            vals = [x["ratio_value"] for x in rows if x["ratio_value"] is not None and math.isfinite(x["ratio_value"])]
            mcs = [x["market_cap"] or 0 for x in rows if x["market_cap"] is not None]
            if len(vals) < 10: continue
            n = len(vals)
            median_ew = _median(vals)
            median_mc = _weighted_quantile(vals, [max(m, 0.01) for m in mcs], 0.5) if len(mcs) == n else median_ew
            p25 = _percentile(vals, 25)
            p75 = _percentile(vals, 75)
            now = datetime.now(timezone.utc).isoformat()
            await db.prepare(
                "INSERT OR REPLACE INTO sector_benchmarks (sector_name, benchmark_type, ratio_code, period_key, median_ew, median_mc, p25, p75, n_peers, reliability, computed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            ).bind("bist_all", "market", rc, period_key, median_ew, median_mc, p25, p75, n, "HIGH", now).run()
            results.append({"ratio": rc, "n": n})
        return results

    # ─── Score Computation ─────────────────────────────────────────────

    async def _compute_scores(self, params):
        db = self.env.TEMEL_DB
        try: cursor = int(params.get("cursor", "0"))
        except: cursor = 0
        batch_size = 20
        _log("compute_scores_start", {"cursor": cursor})

        companies = await db.prepare("SELECT ticker, sector_main, market_cap FROM companies WHERE is_active = 1 ORDER BY ticker LIMIT ? OFFSET ?").bind(batch_size, cursor).all()
        rows = [dict(r) for r in companies.results]
        if not rows:
            _log("compute_scores_done", {"done": True})
            return Response.json({"computed": 0, "total": 0, "cursor": 0, "done": True})

        total_r = await db.prepare("SELECT COUNT(*) as cnt FROM companies WHERE is_active = 1").first()
        total = total_r["cnt"] if total_r else 0

        results = []
        for company in rows:
            tik = company["ticker"]
            sec = company["sector_main"]
            try:
                result = await self._score_single_company(db, tik, sec)
                results.append({"ticker": tik, "score": result.get("composite_score") if result else None})
            except Exception as e:
                results.append({"ticker": tik, "error": str(e)[:100]})

        new_cursor = cursor + batch_size
        if new_cursor >= total:
            new_cursor = 0

        _log("compute_scores_done", {"computed": len(results), "cursor": new_cursor, "done": new_cursor == 0})
        return Response.json({"computed": len(results), "total": total, "cursor": new_cursor, "results": results})

    async def _score_single_company(self, db, ticker, sector_main):
        period_key = "TTM"
        consolidated = _get_consolidated(sector_main)

        r = await db.prepare(
            "SELECT ratio_code, ratio_value FROM company_ratios WHERE ticker = ? AND period_key = ? AND calculation_method = 'v2' AND ratio_value IS NOT NULL"
        ).bind(ticker, period_key).all()
        company_ratios = {}
        for row in r.results:
            company_ratios[row["ratio_code"]] = row["ratio_value"]

        if not company_ratios:
            return {}

        bench_info = await self._resolve_benchmark(db, sector_main, consolidated)
        if not bench_info:
            return {}

        # Build peer map using sector/group peers (batched)
        rc_list = list(company_ratios.keys())
        placeholders = ",".join("?" for _ in rc_list)
        if bench_info["type"] == "sector":
            pr = await db.prepare(
                f"SELECT ratio_code, ratio_value FROM company_ratios WHERE ratio_code IN ({placeholders}) AND period_key = ? AND calculation_method = 'v2' AND ratio_value IS NOT NULL AND ticker != ? AND ticker IN (SELECT ticker FROM companies WHERE sector_main = ? AND is_active = 1)"
            ).bind(*rc_list, period_key, ticker, sector_main).all()
        elif bench_info["type"] == "group":
            pr = await db.prepare(
                f"SELECT cr.ratio_code, cr.ratio_value FROM company_ratios cr JOIN companies c ON cr.ticker = c.ticker JOIN sector_consolidation sc ON c.sector_main = sc.sector_raw WHERE cr.ratio_code IN ({placeholders}) AND cr.period_key = ? AND cr.calculation_method = 'v2' AND cr.ratio_value IS NOT NULL AND cr.ticker != ? AND sc.sector_consolidated = ?"
            ).bind(*rc_list, period_key, ticker, bench_info["name"]).all()
        else:
            pr = await db.prepare(
                f"SELECT ratio_code, ratio_value FROM company_ratios WHERE ratio_code IN ({placeholders}) AND period_key = ? AND calculation_method = 'v2' AND ratio_value IS NOT NULL AND ticker != ?"
            ).bind(*rc_list, period_key, ticker).all()
        peer_map = {}
        for row in pr.results:
            val = row["ratio_value"]
            if val is not None and math.isfinite(val):
                peer_map.setdefault(row["ratio_code"], []).append(val)

        # Get benchmarks (batched)
        bench_data = {}
        br = await db.prepare(
            f"SELECT ratio_code, median_ew, p25, p75, n_peers, reliability FROM sector_benchmarks WHERE sector_name = ? AND benchmark_type = ? AND ratio_code IN ({placeholders}) AND period_key = ?"
        ).bind(bench_info["name"], bench_info["type"], *rc_list, period_key).all()
        for row in br.results:
            bench_data[row["ratio_code"]] = {
                "median_ew": row["median_ew"], "p25": row["p25"], "p75": row["p75"],
                "n_peers": row["n_peers"], "reliability": row["reliability"],
            }

        # Compute pillars
        config = _get_pillar_config(sector_main)
        pillar_scores = {}
        pillar_details = {}
        total_weight_used = 0.0
        weighted_composite = 0.0

        for pillar_name, pillar_cfg in config.items():
            ratios_cfg = pillar_cfg["ratios"]
            weight = pillar_cfg["weight"]
            min_ratios = pillar_cfg["min_ratios"]
            scores_available = []
            total_rw = 0.0
            details = []

            for rc, rw in ratios_cfg.items():
                if rc not in company_ratios: continue
                value = company_ratios[rc]
                if value is None: continue
                peers = peer_map.get(rc, [])
                hib = HIGHER_IS_BETTER.get(rc, True)
                raw_score, peer_median = _sigmoid_score(value, peers, hib)
                if raw_score is None:
                    bench = bench_data.get(rc, {})
                    if bench and bench.get("n_peers", 0) >= 3:
                        med = bench.get("median_ew")
                        if med is not None:
                            raw_score, _ = _sigmoid_score(value, [med], hib)
                if raw_score is None: continue

                bench = bench_data.get(rc, {})
                rel = bench.get("reliability", "HIGH") if bench else "HIGH"
                final_score = _reliability_dampening(raw_score, rel)
                if final_score is None: continue

                scores_available.append((final_score, rw))
                total_rw += rw
                details.append({
                    "ratio_code": rc, "ratio_value": value, "peer_median": peer_median,
                    "raw_score": round(raw_score, 2), "final_score": round(final_score, 2),
                    "higher_is_better": 1 if hib else 0, "reliability": rel,
                })

            if len(scores_available) >= min_ratios and total_rw > 0:
                pscore = sum(s * (w / total_rw) for s, w in scores_available)
                pillar_scores[pillar_name] = round(pscore, 2)
                pillar_details[pillar_name] = details
                weighted_composite += pscore * weight
                total_weight_used += weight

        if total_weight_used < 0.3 or not pillar_scores:
            return {}

        composite = round(weighted_composite / total_weight_used, 2)
        abs_data = self._compute_absolute_score(company_ratios)

        n_expected = sum(len(p["ratios"]) for p in config.values())
        n_available = sum(len(d) for d in pillar_details.values())
        completeness = _safe_div(n_available, n_expected) or 0.0
        rel = "HIGH" if completeness >= 0.7 else "MEDIUM" if completeness >= 0.4 else "LOW"

        now = datetime.now(timezone.utc).isoformat()
        existing = await db.prepare(
            "SELECT id FROM company_scores WHERE ticker = ? AND period_key = ? AND score_version = 'v1'"
        ).bind(ticker, period_key).first()
        score_id = None

        def _detail_stmts(sid):
            stmts = []
            for pname, dets in pillar_details.items():
                for d in dets:
                    stmts.append(
                        db.prepare(
                            "INSERT INTO company_score_details (score_id, ratio_code, ratio_value, peer_median, raw_score, final_score, higher_is_better, reliability, pillar) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                        ).bind(
                            sid, d["ratio_code"], d["ratio_value"], d["peer_median"],
                            d["raw_score"], d["final_score"], d["higher_is_better"], d["reliability"], pname,
                        )
                    )
            return stmts

        if existing:
            score_id = existing["id"]
            await db.batch([
                db.prepare(
                    "UPDATE company_scores SET composite_score = ?, reliability = ?, pillar_finansal_saglik = ?, pillar_karlilik_buyume = ?, pillar_degerleme = ?, benchmark_source = ?, n_peers = ?, data_completeness = ?, upper_sector_name = ?, upper_benchmark_type = ?, absolute_score = ?, absolute_label = ?, computed_at = ? WHERE id = ?"
                ).bind(
                    composite, rel,
                    pillar_scores.get("finansal_saglik"), pillar_scores.get("karlilik_buyume"), pillar_scores.get("degerleme"),
                    bench_info["type"], bench_info.get("n_peers"), round(completeness, 2),
                    bench_info.get("name"), bench_info.get("type"),
                    abs_data["score"], abs_data["label"], now, score_id
                ),
                db.prepare("DELETE FROM company_score_details WHERE score_id = ?").bind(score_id),
                *_detail_stmts(score_id),
            ])
        else:
            batch = [
                db.prepare(
                    "INSERT INTO company_scores (ticker, period_key, composite_score, reliability, pillar_finansal_saglik, pillar_karlilik_buyume, pillar_degerleme, benchmark_source, n_peers, data_completeness, upper_sector_name, upper_benchmark_type, absolute_score, absolute_label, score_version, computed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'v1', ?)"
                ).bind(
                    ticker, period_key, composite, rel,
                    pillar_scores.get("finansal_saglik"), pillar_scores.get("karlilik_buyume"), pillar_scores.get("degerleme"),
                    bench_info["type"], bench_info.get("n_peers"), round(completeness, 2),
                    bench_info.get("name"), bench_info.get("type"),
                    abs_data["score"], abs_data["label"], now
                ),
            ]
            results = await db.batch(batch)
            if results[0].success:
                score_id = results[0].meta.get("last_row_id")
                if score_id:
                    await db.batch(_detail_stmts(score_id))

        return {
            "ticker": ticker, "composite_score": composite, "reliability": rel,
            "pillars": pillar_scores, "absolute_score": abs_data["score"], "absolute_label": abs_data["label"],
            "benchmark": bench_info,
        }

    async def _resolve_benchmark(self, db, sector_main, consolidated):
        r = await db.prepare("SELECT COUNT(*) as cnt FROM companies WHERE sector_main = ? AND is_active = 1").bind(sector_main).first()
        n_sector = r["cnt"] if r else 0
        if n_sector >= 5:
            return {"type": "sector", "name": sector_main, "n_peers": n_sector}
        if consolidated:
            r2 = await db.prepare(
                "SELECT COUNT(*) as cnt FROM companies c JOIN sector_consolidation sc ON c.sector_main = sc.sector_raw WHERE sc.sector_consolidated = ? AND c.is_active = 1"
            ).bind(consolidated).first()
            n_group = r2["cnt"] if r2 else 0
            if n_group >= 3:
                return {"type": "group", "name": consolidated, "n_peers": n_group}
        mr = await db.prepare("SELECT COUNT(*) as cnt FROM companies WHERE is_active = 1").first()
        n_market = mr["cnt"] if mr else 0
        return {"type": "market", "name": "bist_all", "n_peers": n_market}

    def _compute_absolute_score(self, ratios):
        pillars_found = {p: [] for p in ["finansal_saglik", "karlilik_buyume", "degerleme"]}
        for pname, pcfg in PILLAR_CONFIG["_default"].items():
            for rc, rw in pcfg["ratios"].items():
                if rc in ABSOLUTE_THRESHOLDS and rc in ratios:
                    sc = _absolute_ratio_score(ratios[rc], ABSOLUTE_THRESHOLDS[rc])
                    if sc is not None:
                        pillars_found[pname].append((sc, rw))
        weighted = []
        total_w = 0.0
        for pname, pcfg in PILLAR_CONFIG["_default"].items():
            items = pillars_found[pname]
            if items:
                pscore = sum(s * w for s, w in items) / sum(w for _, w in items)
                weighted.append((pscore, pcfg["weight"]))
                total_w += pcfg["weight"]
        if not weighted or total_w < 0.3:
            return {"score": None, "label": None}
        total = sum(s * (w / total_w) for s, w in weighted)
        label = "KRITIK"
        for threshold, lbl in ABSOLUTE_LABELS:
            if total >= threshold:
                label = lbl
                break
        return {"score": round(total, 1), "label": label}

    # ─── Score Card ────────────────────────────────────────────────────

    async def _get_score(self, ticker, params, kv=None, cache_key=None):
        db = self.env.TEMEL_DB
        ticker = ticker.upper()

        company = await db.prepare("SELECT ticker, name, sector_main FROM companies WHERE ticker = ?").bind(ticker).first()
        if not company:
            return Response.json({"error": "not found"}, status=404)

        score = await db.prepare(
            "SELECT * FROM company_scores WHERE ticker = ? AND period_key = 'TTM' AND score_version = 'v1' ORDER BY computed_at DESC LIMIT 1"
        ).bind(ticker).first()
        s = dict(score) if score else None

        ratios = await db.prepare(
            "SELECT ratio_code, ratio_value FROM company_ratios WHERE ticker = ? AND period_key = 'TTM' AND calculation_method = 'v2'"
        ).bind(ticker).all()
        ratio_map = {r["ratio_code"]: r["ratio_value"] for r in ratios.results}

        if not s:
            data = {
                "ticker": ticker,
                "company_name": company["name"],
                "sector": company["sector_main"],
                "score": None, "ratios": ratio_map,
            }
            return await _cached_json(kv, cache_key, data)

        details = await db.prepare("SELECT * FROM company_score_details WHERE score_id = ?").bind(s["id"]).all()
        detail_list = [dict(d) for d in details.results]

        sector_rank = await self._calc_rank(db, ticker, company["sector_main"], "sector")
        consolidated = _get_consolidated(company["sector_main"])
        group_rank = None
        if consolidated:
            group_rank = await self._calc_rank(db, ticker, consolidated, "group")

        def pillar_details(pname):
            return [{
                "ratio_code": d["ratio_code"], "ratio_value": d["ratio_value"],
                "peer_median": d["peer_median"], "raw_score": d["raw_score"],
                "final_score": d["final_score"], "reliability": d["reliability"],
            } for d in detail_list if d.get("pillar") == pname]

        data = {
            "ticker": ticker,
            "company_name": company["name"],
            "sector": company["sector_main"],
            "composite_score": s["composite_score"],
            "reliability": s["reliability"],
            "pillars": {
                "finansal_saglik": {"score": s["pillar_finansal_saglik"], "details": pillar_details("finansal_saglik")},
                "karlilik_buyume": {"score": s["pillar_karlilik_buyume"], "details": pillar_details("karlilik_buyume")},
                "degerleme": {"score": s["pillar_degerleme"], "details": pillar_details("degerleme")},
            },
            "absolute": {"score": s["absolute_score"], "label": s["absolute_label"]},
            "benchmark": {
                "source": s["benchmark_source"], "name": s["upper_sector_name"],
                "n_peers": s["n_peers"], "data_completeness": s["data_completeness"],
            },
            "ranks": {"sector": sector_rank, "group": group_rank},
            "ratios": ratio_map,
        }
        return await _cached_json(kv, cache_key, data)

    async def _calc_rank(self, db, ticker, scope_name, scope_type):
        if scope_type == "sector":
            r = await db.prepare("SELECT cs.composite_score FROM company_scores cs JOIN companies c ON cs.ticker = c.ticker WHERE c.sector_main = ? AND cs.period_key = 'TTM' AND cs.score_version = 'v1' AND cs.composite_score IS NOT NULL").bind(scope_name).all()
        elif scope_type == "group":
            r = await db.prepare("SELECT cs.composite_score FROM company_scores cs JOIN companies c ON cs.ticker = c.ticker JOIN sector_consolidation sc ON c.sector_main = sc.sector_raw WHERE sc.sector_consolidated = ? AND cs.period_key = 'TTM' AND cs.score_version = 'v1' AND cs.composite_score IS NOT NULL").bind(scope_name).all()
        else:
            return None
        scores = [row["composite_score"] for row in r.results if row["composite_score"] is not None]
        if not scores: return None
        own = await db.prepare("SELECT composite_score FROM company_scores WHERE ticker = ? AND period_key = 'TTM' AND score_version = 'v1' AND composite_score IS NOT NULL").bind(ticker).first()
        if not own: return None
        ov = own["composite_score"]
        below = sum(1 for s in scores if s < ov)
        equal = sum(1 for s in scores if s == ov)
        pct = (below + 0.5 * equal) / len(scores) * 100
        return {"percentile": round(pct, 1), "n_peers": len(scores)}

    # ─── Rankings ──────────────────────────────────────────────────────

    async def _get_rankings(self, remaining, params, kv=None, cache_key=None):
        db = self.env.TEMEL_DB
        parts = remaining.split("/")
        scope_type = parts[0] if parts else "market"
        scope_name = parts[1] if len(parts) > 1 else None
        limit = min(int(params.get("limit", "50")), 200)
        offset = int(params.get("offset", "0"))

        if scope_type == "sector" and scope_name:
            cond = "c.sector_main = ?"
            bind_val = scope_name
        elif scope_type == "group" and scope_name:
            cond = "c.sector_main IN (SELECT sector_raw FROM sector_consolidation WHERE sector_consolidated = ?)"
            bind_val = scope_name
        elif scope_type == "market":
            cond = "1=1"
            bind_val = None
        else:
            return Response.json({"error": "invalid scope"}, status=400)

        if bind_val:
            r = await db.prepare(
                f"SELECT cs.ticker, c.name, c.sector_main, cs.composite_score, cs.reliability, cs.pillar_finansal_saglik, cs.pillar_karlilik_buyume, cs.pillar_degerleme, c.market_cap FROM company_scores cs JOIN companies c ON cs.ticker = c.ticker WHERE cs.period_key = 'TTM' AND cs.score_version = 'v1' AND cs.composite_score IS NOT NULL AND {cond} ORDER BY cs.composite_score DESC LIMIT ? OFFSET ?"
            ).bind(bind_val, limit, offset).all()
            cr = await db.prepare(
                f"SELECT COUNT(*) as cnt FROM company_scores cs JOIN companies c ON cs.ticker = c.ticker WHERE cs.period_key = 'TTM' AND cs.score_version = 'v1' AND cs.composite_score IS NOT NULL AND {cond}"
            ).bind(bind_val).first()
        else:
            r = await db.prepare(
                "SELECT cs.ticker, c.name, c.sector_main, cs.composite_score, cs.reliability, cs.pillar_finansal_saglik, cs.pillar_karlilik_buyume, cs.pillar_degerleme, c.market_cap FROM company_scores cs JOIN companies c ON cs.ticker = c.ticker WHERE cs.period_key = 'TTM' AND cs.score_version = 'v1' AND cs.composite_score IS NOT NULL ORDER BY cs.composite_score DESC LIMIT ? OFFSET ?"
            ).bind(limit, offset).all()
            cr = await db.prepare(
                "SELECT COUNT(*) as cnt FROM company_scores WHERE period_key = 'TTM' AND score_version = 'v1' AND composite_score IS NOT NULL"
            ).first()

        total = cr["cnt"] if cr else 0
        rows = [dict(x) for x in r.results]
        for i, row in enumerate(rows):
            row["rank"] = offset + i + 1

        data = {"scope": scope_type, "name": scope_name, "total": total, "limit": limit, "offset": offset, "results": rows}
        return await _cached_json(kv, cache_key, data)

    # ─── Comparison ────────────────────────────────────────────────────

    async def _compare(self, tickers_str, kv=None, cache_key=None):
        db = self.env.TEMEL_DB
        parts = tickers_str.split(",")
        tickers = [t.upper().strip() for t in parts if t.strip()]
        if len(tickers) < 2:
            return Response.json({"error": "at least 2 tickers required"}, status=400)
        if len(tickers) > 5:
            return Response.json({"error": "max 5 tickers"}, status=400)

        results = []
        for t in tickers:
            company = await db.prepare("SELECT ticker, name, sector_main FROM companies WHERE ticker = ?").bind(t).first()
            if not company: continue
            score = await db.prepare(
                "SELECT * FROM company_scores WHERE ticker = ? AND period_key = 'TTM' AND score_version = 'v1' ORDER BY computed_at DESC LIMIT 1"
            ).bind(t).first()
            s = dict(score) if score else {}
            ratios = await db.prepare("SELECT ratio_code, ratio_value FROM company_ratios WHERE ticker = ? AND period_key = 'TTM' AND calculation_method = 'v2'").bind(t).all()
            rm = {r["ratio_code"]: r["ratio_value"] for r in ratios.results}
            results.append({
                "ticker": t, "company_name": company["name"], "sector": company["sector_main"],
                "composite_score": s.get("composite_score"), "reliability": s.get("reliability"),
                "pillars": {
                    "finansal_saglik": s.get("pillar_finansal_saglik"),
                    "karlilik_buyume": s.get("pillar_karlilik_buyume"),
                    "degerleme": s.get("pillar_degerleme"),
                },
                "absolute": {"score": s.get("absolute_score"), "label": s.get("absolute_label")},
                "key_ratios": {rc: rm.get(rc) for rc in ["pe", "pb", "roe", "net_margin", "current_ratio", "debt_equity"]},
            })
        data = {"tickers": results}
        return await _cached_json(kv, cache_key, data)

    # ─── Absolute Score ────────────────────────────────────────────────

    async def _get_absolute(self, ticker, kv=None, cache_key=None):
        db = self.env.TEMEL_DB
        ticker = ticker.upper()
        company = await db.prepare("SELECT ticker, name, sector_main FROM companies WHERE ticker = ?").bind(ticker).first()
        if not company:
            return Response.json({"error": "not found"}, status=404)

        ratios = await db.prepare("SELECT ratio_code, ratio_value FROM company_ratios WHERE ticker = ? AND period_key = 'TTM' AND calculation_method = 'v2'").bind(ticker).all()
        ratio_map = {r["ratio_code"]: r["ratio_value"] for r in ratios.results}
        ratio_scores = {}
        for rc, thresholds in ABSOLUTE_THRESHOLDS.items():
            val = ratio_map.get(rc)
            if val is not None:
                ratio_scores[rc] = _absolute_ratio_score(val, thresholds)

        abs_data = self._compute_absolute_score(ratio_map)
        label_tr = {"GUCLU": "Güçlü", "SAGLIKLI": "Sağlıklı", "ORTA": "Orta", "ZAYIF": "Zayıf", "KRITIK": "Kritik"}
        data = {
            "ticker": ticker, "company_name": company["name"], "sector": company["sector_main"],
            "score": abs_data["score"], "label": abs_data["label"],
            "label_tr": label_tr.get(abs_data["label"]),
            "ratio_scores": ratio_scores,
        }
        return await _cached_json(kv, cache_key, data)

    # ─── Sector List & Detail ──────────────────────────────────────────

    async def _list_sectors(self, kv=None, cache_key=None):
        db = self.env.TEMEL_DB
        sectors = await db.prepare("SELECT sector_main, COUNT(*) as cnt FROM companies WHERE is_active = 1 GROUP BY sector_main ORDER BY cnt DESC").all()
        groups = await db.prepare("SELECT sc.sector_consolidated, COUNT(*) as cnt FROM companies c JOIN sector_consolidation sc ON c.sector_main = sc.sector_raw WHERE sc.sector_consolidated IS NOT NULL AND c.is_active = 1 GROUP BY sc.sector_consolidated ORDER BY cnt DESC").all()

        sector_list = []
        for row in sectors.results:
            d = dict(row)
            cons = _get_consolidated(d["sector_main"])
            d["consolidated"] = cons
            d["consolidated_name"] = SECTOR_GROUP_NAMES.get(cons) if cons else None
            sector_list.append(d)

        group_list = [{"key": g["sector_consolidated"], "name": SECTOR_GROUP_NAMES.get(g["sector_consolidated"], g["sector_consolidated"]), "count": g["cnt"]} for g in groups.results]

        return await _cached_json(kv, cache_key, {"sectors": sector_list, "groups": group_list})

    async def _sector_detail(self, name, params, kv=None, cache_key=None):
        db = self.env.TEMEL_DB
        limit = min(int(params.get("limit", "50")), 200)
        original_name = name

        # Try raw name first (with underscores -> spaces for sector_main matching)
        name_with_spaces = name.replace("_", " ")
        sector_info = await db.prepare("SELECT sector_main, COUNT(*) as cnt FROM companies WHERE sector_main = ? AND is_active = 1 GROUP BY sector_main").bind(name_with_spaces).first()
        if sector_info:
            data = await self._single_sector_detail(db, name_with_spaces, sector_info["cnt"], limit)
            return await _cached_json(kv, cache_key, data)

        # Try as consolidated group key (underscore format preserved)
        for k, v in SECTOR_GROUP_NAMES.items():
            if v.lower().replace(" ", "_").replace("&", "ve") == original_name.lower().replace(" ", "_").replace("&", "ve") or v.lower() == original_name.lower():
                data = await self._group_detail(db, k, limit)
                return await _cached_json(kv, cache_key, data)
            if k.lower() == original_name.lower():
                data = await self._group_detail(db, k, limit)
                return await _cached_json(kv, cache_key, data)
        for k, v in SECTOR_CONSOLIDATION.items():
            if v and (v == original_name or v.lower() == original_name.lower()):
                data = await self._group_detail(db, v, limit)
                return await _cached_json(kv, cache_key, data)
            if k.lower() == original_name.lower():
                c = SECTOR_CONSOLIDATION.get(k)
                if c:
                    data = await self._group_detail(db, c, limit)
                    return await _cached_json(kv, cache_key, data)
            if v and v.lower().replace("_", "") == original_name.lower().replace("_", ""):
                data = await self._group_detail(db, v, limit)
                return await _cached_json(kv, cache_key, data)

        # Last resort: try name_with_spaces against consolidation keys/values
        for k, v in SECTOR_CONSOLIDATION.items():
            if v and (v.replace("_", " ") == name_with_spaces or v.replace("_", " ").lower() == name_with_spaces.lower()):
                data = await self._group_detail(db, v, limit)
                return await _cached_json(kv, cache_key, data)
            if k.lower() == name_with_spaces.lower():
                c = SECTOR_CONSOLIDATION.get(k)
                if c:
                    data = await self._group_detail(db, c, limit)
                    return await _cached_json(kv, cache_key, data)

        return Response.json({"error": "sector not found"}, status=404)

    async def _single_sector_detail(self, db, name, n, limit):
        benchmarks = await db.prepare("SELECT * FROM sector_benchmarks WHERE sector_name = ? AND benchmark_type = 'sector' AND period_key = 'TTM' ORDER BY ratio_code").bind(name).all()
        bench_map = {}
        for b in benchmarks.results:
            bench_map[b["ratio_code"]] = {
                "median_ew": b["median_ew"], "p25": b["p25"], "p75": b["p75"],
                "n_peers": b["n_peers"], "reliability": b["reliability"],
            }

        leaders = await db.prepare(
            "SELECT cs.ticker, c.name, cs.composite_score, cs.pillar_finansal_saglik, cs.pillar_karlilik_buyume, cs.pillar_degerleme, cs.reliability, c.market_cap FROM company_scores cs JOIN companies c ON cs.ticker = c.ticker WHERE c.sector_main = ? AND cs.period_key = 'TTM' AND cs.score_version = 'v1' AND cs.composite_score IS NOT NULL ORDER BY cs.composite_score DESC LIMIT ?"
        ).bind(name, limit).all()

        leader_list = []
        scores = []
        mcs = []
        for i, row in enumerate(leaders.results):
            d = dict(row)
            d["rank"] = i + 1
            leader_list.append(d)
            if d["composite_score"] is not None:
                scores.append(d["composite_score"])
                mcs.append(d["market_cap"] or 0)

        sector_score_ew = _median(scores) if scores else None
        sector_score_mc = _weighted_quantile(scores, [max(m, 0.01) for m in mcs], 0.5) if scores and len(mcs) == len(scores) else sector_score_ew

        return {
            "sector": name, "company_count": n,
            "benchmarks": bench_map,
            "sector_score": {"equal_weight": sector_score_ew, "market_cap_weighted": sector_score_mc},
            "leaderboard": leader_list,
        }

    async def _group_detail(self, db, key, limit):
        r = await db.prepare("SELECT COUNT(*) as cnt FROM companies c JOIN sector_consolidation sc ON c.sector_main = sc.sector_raw WHERE sc.sector_consolidated = ? AND c.is_active = 1").bind(key).first()
        n = r["cnt"] if r else 0

        benchmarks = await db.prepare("SELECT * FROM sector_benchmarks WHERE sector_name = ? AND benchmark_type = 'group' AND period_key = 'TTM' ORDER BY ratio_code").bind(key).all()
        bench_map = {}
        for b in benchmarks.results:
            bench_map[b["ratio_code"]] = {
                "median_ew": b["median_ew"], "p25": b["p25"], "p75": b["p75"],
                "n_peers": b["n_peers"], "reliability": b["reliability"],
            }

        leaders = await db.prepare(
            "SELECT cs.ticker, c.name, c.sector_main, cs.composite_score, cs.pillar_finansal_saglik, cs.pillar_karlilik_buyume, cs.pillar_degerleme, cs.reliability, c.market_cap FROM company_scores cs JOIN companies c ON cs.ticker = c.ticker JOIN sector_consolidation sc ON c.sector_main = sc.sector_raw WHERE sc.sector_consolidated = ? AND cs.period_key = 'TTM' AND cs.score_version = 'v1' AND cs.composite_score IS NOT NULL ORDER BY cs.composite_score DESC LIMIT ?"
        ).bind(key, limit).all()

        leader_list = []
        scores = []
        mcs = []
        for i, row in enumerate(leaders.results):
            d = dict(row)
            d["rank"] = i + 1
            leader_list.append(d)
            if d["composite_score"] is not None:
                scores.append(d["composite_score"])
                mcs.append(d["market_cap"] or 0)

        sector_score_ew = _median(scores) if scores else None
        sector_score_mc = _weighted_quantile(scores, [max(m, 0.01) for m in mcs], 0.5) if scores and len(mcs) == len(scores) else sector_score_ew

        return {
            "group": SECTOR_GROUP_NAMES.get(key, key), "company_count": n,
            "benchmarks": bench_map,
            "sector_score": {"equal_weight": sector_score_ew, "market_cap_weighted": sector_score_mc},
            "leaderboard": leader_list,
        }
