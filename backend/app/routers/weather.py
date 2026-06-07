from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services import maps, weather, geocoding

router = APIRouter()


class RouteRequest(BaseModel):
    from_: str
    to_: str
    departure_time: str | None = None
    via: list[str] = []


@router.post("/weather-route")
def get_weather_route(req: RouteRequest):
    route_data = maps.get_route_data(req.from_, req.to_, req.departure_time, req.via)
    waypoints = route_data["waypoints"]
    if not waypoints:
        raise HTTPException(status_code=404, detail="ルートが見つかりませんでした")

    # 天気は並列取得（Open-Meteo は安定）
    weather_results = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(weather.get_weather, lat, lon, timestamp): i
            for i, (timestamp, lat, lon) in enumerate(waypoints)
        }
        for future in as_completed(futures):
            weather_results[futures[future]] = future.result()

    # 住所は逐次取得（Nominatim: 1 req/sec 制限）
    results = []
    for i, (timestamp, lat, lon) in enumerate(waypoints):
        address = geocoding.get_address(lat, lon)
        results.append({
            "index": i,
            "timestamp": timestamp,
            "lat": lat,
            "lon": lon,
            "address": address,
            **weather_results[i],
        })

    return {"waypoints": results, "route": route_data["route"]}
