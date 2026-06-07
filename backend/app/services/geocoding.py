import requests

NOMINATIM = "http://nominatim:8080"
HEADERS = {"User-Agent": "Weayther/1.0", "Accept-Language": "ja"}

_cache: dict[tuple, str] = {}


def get_address(lat: float, lon: float) -> str:
    key = (round(lat, 3), round(lon, 3))
    if key in _cache:
        return _cache[key]

    for attempt in range(4):
        try:
            resp = requests.get(
                f"{NOMINATIM}/reverse",
                params={"lat": lat, "lon": lon, "format": "json"},
                headers=HEADERS,
                timeout=10,
            )
            if resp.status_code in (429, 502, 503, 504):
                import time; time.sleep(1.0 * (attempt + 1))
                continue
            resp.raise_for_status()
            result = resp.json().get("display_name", f"{lat:.4f}, {lon:.4f}")
            _cache[key] = result
            return result
        except requests.exceptions.RequestException:
            import time; time.sleep(1.0 * (attempt + 1))

    return f"{lat:.4f}, {lon:.4f}"
