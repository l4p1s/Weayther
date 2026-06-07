export async function fetchWeatherRoute(from_, to_, departureTime, via) {
  const body = { from_, to_, via: via ?? [] };
  if (departureTime) body.departure_time = departureTime;

  const res = await fetch("/api/weather-route", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? "APIエラーが発生しました");
  }
  return res.json();
}
