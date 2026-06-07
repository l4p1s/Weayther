import time
import requests

_WMO_CODES = {
    0: "快晴", 1: "ほぼ晴れ", 2: "一部曇り", 3: "曇り",
    45: "霧", 48: "着氷性の霧",
    51: "小雨（霧雨）", 53: "霧雨", 55: "強い霧雨",
    61: "小雨", 63: "雨", 65: "大雨",
    71: "小雪", 73: "雪", 75: "大雪",
    80: "にわか雨", 81: "雨", 82: "強いにわか雨",
    95: "雷雨", 96: "雷雨（ひょうあり）", 99: "激しい雷雨",
}

# (lat_rounded, lon_rounded, timestamp) → weather dict
_cache: dict[tuple, dict] = {}


def get_weather(lat: float, lon: float, timestamp: str) -> dict:
    # 0.1度単位（約10km）でキャッシュ：近距離の同時刻は同じ天気とみなす
    cache_key = (round(lat, 1), round(lon, 1), timestamp)
    if cache_key in _cache:
        return _cache[cache_key]

    date_part, hour_part = timestamp.split(":")
    target_time = f"{date_part}T{hour_part}:00"

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,windspeed_10m,weathercode"
        f"&timezone=auto&forecast_days=2"
    )

    for attempt in range(4):
        response = requests.get(url, timeout=10)
        if response.status_code in (429, 502, 503, 504):
            time.sleep(1.5 * (attempt + 1))
            continue
        response.raise_for_status()
        break
    else:
        return {"temp": None, "wind_spd": None, "condition": "天気取得失敗"}

    data = response.json()
    times = data["hourly"]["time"]
    if target_time not in times:
        result = {"temp": None, "wind_spd": None, "condition": "データなし"}
    else:
        idx = times.index(target_time)
        code = data["hourly"]["weathercode"][idx]
        result = {
            "temp": data["hourly"]["temperature_2m"][idx],
            "wind_spd": round(data["hourly"]["windspeed_10m"][idx] / 3.6, 1),
            "condition": _WMO_CODES.get(code, f"コード {code}"),
        }

    _cache[cache_key] = result
    return result
