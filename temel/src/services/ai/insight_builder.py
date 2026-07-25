from typing import Optional, List


class InsightBuilder:
    def build(self, ratios: dict, benchmarks: Optional[dict], trends: Optional[dict], sector: Optional[str] = None) -> list:
        insights = []
        if not ratios:
            return [{"insight": "Finansal rasyo verisi mevcut değil", "category": "info", "importance": 1}]

        rc_data = ratios.get("ratios", {})
        missing = ratios.get("missing_ratios", [])

        for code, entry in rc_data.items():
            value = entry.get("value")
            if value is None:
                continue
            ctx = entry.get("sector_context")
            trend_data = trends.get("trends", {}).get(code) if trends else None

            if ctx:
                med = ctx.get("median")
                if med and med != 0:
                    vs_median = (value - med) / abs(med)
                    hib = entry.get("higher_is_better", True)
                    outperforming = (vs_median > 0.2 and hib) or (vs_median < -0.2 and not hib)
                    underperforming = (vs_median < -0.2 and hib) or (vs_median > 0.2 and not hib)

                    if outperforming:
                        pct = abs(vs_median) * 100
                        insights.append({
                            "insight": f"{entry['name']} sektör ortalamasının %{pct:.0f} üzerinde ({value:.2f} vs {med:.2f})",
                            "category": "strength",
                            "importance": 4 if pct > 50 else 3,
                            "data": {"ratio": code, "value": value, "sector_median": med},
                        })
                    elif underperforming:
                        pct = abs(vs_median) * 100
                        insights.append({
                            "insight": f"{entry['name']} sektör ortalamasının %{pct:.0f} altında ({value:.2f} vs {med:.2f})",
                            "category": "weakness",
                            "importance": 4 if pct > 50 else 3,
                            "data": {"ratio": code, "value": value, "sector_median": med},
                        })

            if trend_data:
                direction = trend_data.get("direction")
                yoy = trend_data.get("yoy_change")
                if direction == "rising" and yoy and yoy > 0.1:
                    insights.append({
                        "insight": f"{entry['name']} yükseliş trendinde (Yıllık %{yoy*100:.0f} artış)",
                        "category": "positive_trend",
                        "importance": 3,
                        "data": {"ratio": code, "trend": direction, "yoy_change": yoy},
                    })
                elif direction == "falling" and yoy and yoy < -0.1:
                    insights.append({
                        "insight": f"{entry['name']} düşüş trendinde (Yıllık %{abs(yoy)*100:.0f} azalış)",
                        "category": "negative_trend",
                        "importance": 3,
                        "data": {"ratio": code, "trend": direction, "yoy_change": yoy},
                    })

        if missing:
            insights.append({
                "insight": f"{len(missing)} rasyo hesaplanamadı: {', '.join(missing[:5])}",
                "category": "data_quality",
                "importance": 2,
                "data": {"missing_ratios": missing[:5]},
            })

        insights.sort(key=lambda x: x["importance"], reverse=True)
        return insights[:10]
