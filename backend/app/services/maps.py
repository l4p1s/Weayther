import bisect
import datetime
import math
import time
import requests
from concurrent.futures import ThreadPoolExecutor

NUM_WAYPOINTS = 12
NOMINATIM = "http://nominatim:8080"
OSRM = "http://router.project-osrm.org"
HEADERS = {"User-Agent": "Weayther/1.0"}


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6_371_000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def _geocode(place: str) -> tuple[float, float]:
    for attempt in range(5):
        try:
            resp = requests.get(
                f"{NOMINATIM}/search",
                params={"q": place, "format": "json", "limit": 1},
                headers=HEADERS,
                timeout=15,
            )
            if resp.status_code in (429, 502, 503, 504):
                time.sleep(2.0 * (attempt + 1))
                continue
            resp.raise_for_status()
            results = resp.json()
            if not results:
                raise ValueError(f"場所が見つかりませんでした: {place}")
            return float(results[0]["lat"]), float(results[0]["lon"])
        except requests.exceptions.RequestException:
            time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(f"ジオコーディング失敗: {place}")


def get_route_data(from_: str, to_: str, departure_time: str | None = None, via: list[str] = []) -> dict:
    all_places = [from_] + via + [to_]
    coords = [_geocode(p) for p in all_places]

    from_lat, from_lon = coords[0]
    to_lat, to_lon = coords[-1]
    via_coords = coords[1:-1]

    waypoint_str = ";".join(
        [f"{from_lon},{from_lat}"]
        + [f"{lon},{lat}" for lat, lon in via_coords]
        + [f"{to_lon},{to_lat}"]
    )

    resp = requests.get(
        f"{OSRM}/route/v1/driving/{waypoint_str}",
        params={"overview": "full", "geometries": "geojson", "steps": "true"},
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    if data.get("code") != "Ok" or not data.get("routes"):
        return {"waypoints": [], "route": []}

    route_obj = data["routes"][0]
    route = [[c[1], c[0]] for c in route_obj["geometry"]["coordinates"]]

    now = datetime.datetime.fromisoformat(departure_time) if departure_time else datetime.datetime.now()

    start = data["waypoints"][0]["location"]
    points = [(0.0, 0.0, start[1], start[0])]
    cum_dist = 0.0
    cum_time = 0.0

    for leg in route_obj["legs"]:
        for step in leg["steps"]:
            coords_list = step["geometry"]["coordinates"]
            speed = step["distance"] / step["duration"] if step["duration"] > 0 else 0
            for i in range(len(coords_list) - 1):
                lon1, lat1 = coords_list[i]
                lon2, lat2 = coords_list[i + 1]
                seg_dist = _haversine(lat1, lon1, lat2, lon2)
                cum_dist += seg_dist
                cum_time += (seg_dist / speed / 60.0) if speed > 0 else 0
                points.append((cum_dist, cum_time, lat2, lon2))

    total_dist = cum_dist
    dists = [p[0] for p in points]

    waypoints = []
    for i in range(NUM_WAYPOINTS):
        target = total_dist * i / (NUM_WAYPOINTS - 1)
        idx = min(bisect.bisect_left(dists, target), len(points) - 1)
        _, t, lat, lon = points[idx]
        cur_time = now + datetime.timedelta(minutes=t)
        waypoints.append((cur_time.strftime("%Y-%m-%d:%H"), lat, lon))

    return {"waypoints": waypoints, "route": route}
