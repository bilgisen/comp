"""Unit tests for score-worker pure functions (no Worker dependencies)."""

import math
import pytest


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


def _safe_div(a, b):
    if a is None or b is None: return None
    try: return a / b if abs(b) > 1e-12 else None
    except: return None


# ─── Tests ────────────────────────────────────────────────────────────────

class TestMedian:
    def test_empty(self):
        assert _median([]) == 0.0

    def test_single(self):
        assert _median([5]) == 5.0

    def test_odd(self):
        assert _median([1, 3, 5]) == 3.0

    def test_even(self):
        assert _median([1, 2, 3, 4]) == 2.5


class TestPercentile:
    def test_empty(self):
        assert _percentile([], 50) == 0.0

    def test_median(self):
        assert _percentile([1, 2, 3, 4, 5], 50) == 3.0

    def test_q25(self):
        assert _percentile([1, 2, 3, 4, 5], 25) == pytest.approx(2.0, abs=0.01)

    def test_q75(self):
        assert _percentile([1, 2, 3, 4, 5], 75) == pytest.approx(4.0, abs=0.01)


class TestRobustStd:
    def test_normal(self):
        vals = [10, 12, 14, 15, 18, 20, 22, 25]
        rs = _robust_std(vals)
        assert rs > 0

    def test_identical(self):
        assert _robust_std([5, 5, 5]) == 0.0

    def test_iqr_ratio(self):
        vals = list(range(1, 101))
        rs = _robust_std(vals)
        std = math.sqrt(sum((x - 50.5) ** 2 for x in vals) / 99)
        assert abs(rs - std) / std < 0.3


class TestWinsorize:
    def test_few_elements(self):
        assert _winsorize([1, 2, 3]) == [1, 2, 3]

    def test_clips_outliers(self):
        vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]
        w = _winsorize(vals, 10.0, 90.0)
        assert max(w) < 100
        assert min(w) >= 1


class TestSigmoidScore:
    def test_above_median(self):
        score, med = _sigmoid_score(100, [10, 20, 30, 40, 50])
        assert score > 50

    def test_below_median(self):
        score, med = _sigmoid_score(10, [100, 200, 300, 400, 500])
        assert score < 50

    def test_higher_is_better_false(self):
        # value=10 is HIGH vs peers [1,2,3,4,5] → penalized (low score)
        score_low, _ = _sigmoid_score(10, [1, 2, 3, 4, 5], higher_is_better=False)
        # value=10 is LOW vs peers [10,20,30,40,50] → rewarded (high score)
        score_high, _ = _sigmoid_score(10, [10, 20, 30, 40, 50], higher_is_better=False)
        assert score_low < score_high

    def test_insufficient_peers(self):
        score, med = _sigmoid_score(10, [1, 2])
        assert score is None

    def test_bounds(self):
        for _ in range(100):
            score, _ = _sigmoid_score(10 + _ * 10, list(range(1, 51)))
            assert 0.01 <= score <= 99.99


class TestReliabilityDampening:
    def test_high(self):
        assert _reliability_dampening(80.0, "HIGH") == 80.0

    def test_medium(self):
        assert _reliability_dampening(80.0, "MEDIUM") == 74.0

    def test_low(self):
        assert _reliability_dampening(80.0, "LOW") == pytest.approx(66.5, abs=0.01)

    def test_unknown(self):
        assert _reliability_dampening(80.0, "INVALID") is None

    def test_below_50(self):
        assert _reliability_dampening(30.0, "MEDIUM") == 34.0


class TestAbsoluteRatioScore:
    THRESHOLDS = [(0.5, 0), (1.0, 25), (2.0, 50), (5.0, 75), (float("inf"), 100)]

    def test_below_min(self):
        assert _absolute_ratio_score(0.1, self.THRESHOLDS) == 0

    def test_mid_range(self):
        assert _absolute_ratio_score(1.5, self.THRESHOLDS) == 50

    def test_above_max(self):
        assert _absolute_ratio_score(10.0, self.THRESHOLDS) == 100

    def test_none(self):
        assert _absolute_ratio_score(None, self.THRESHOLDS) is None


class TestSafeDiv:
    def test_normal(self):
        assert _safe_div(10, 2) == 5.0

    def test_zero_divisor(self):
        assert _safe_div(10, 0) is None

    def test_none_a(self):
        assert _safe_div(None, 2) is None

    def test_none_b(self):
        assert _safe_div(10, None) is None
