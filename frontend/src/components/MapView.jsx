import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const COLORS = { start: "#48bb78", end: "#f56565", mid: "#2b6cb0" };

export default function MapView({ waypoints, route }) {
  const containerRef = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    if (mapRef.current) {
      mapRef.current.remove();
      mapRef.current = null;
    }

    const map = L.map(containerRef.current, { zoomControl: true });
    mapRef.current = map;

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a>",
      maxZoom: 18,
    }).addTo(map);

    if (route.length > 0) {
      L.polyline(route, { color: "#2b6cb0", weight: 5, opacity: 0.75 }).addTo(map);
    }

    const last = waypoints.length - 1;
    waypoints.forEach((wp, i) => {
      const color = i === 0 ? COLORS.start : i === last ? COLORS.end : COLORS.mid;
      const [date, hour] = wp.timestamp.split(":");
      const label = i === 0 ? "出発" : i === last ? "到着" : `通過点 ${i}`;

      L.circleMarker([wp.lat, wp.lon], {
        radius: i === 0 || i === last ? 10 : 8,
        fillColor: color,
        color: "#fff",
        weight: 2,
        fillOpacity: 1,
      })
        .bindPopup(
          `<div style="min-width:160px">
            <b style="color:${color}">${label}</b><br>
            ${wp.address}<br>
            <span style="color:#718096;font-size:12px">${date} ${hour}:00</span><br>
            <br>
            🌡 <b>${wp.temp ?? "—"}°C</b>　💨 ${wp.wind_spd ?? "—"} m/s<br>
            ${wp.condition}
          </div>`,
          { maxWidth: 220 }
        )
        .addTo(map);
    });

    const allPoints = [
      ...route,
      ...waypoints.map((wp) => [wp.lat, wp.lon]),
    ];
    if (allPoints.length > 0) {
      map.fitBounds(L.latLngBounds(allPoints), { padding: [40, 40] });
    }

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [waypoints, route]);

  return (
    <div style={styles.wrapper}>
      <div ref={containerRef} style={styles.map} />
      <div style={styles.legend}>
        <span style={{ color: COLORS.start }}>● 出発</span>
        <span style={{ color: COLORS.mid }}>● 通過点</span>
        <span style={{ color: COLORS.end }}>● 到着</span>
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    position: "relative",
    borderRadius: 12,
    overflow: "hidden",
    boxShadow: "0 2px 16px rgba(0,0,0,0.10)",
  },
  map: { width: "100%", height: "55vh", minHeight: 320 },
  legend: {
    position: "absolute",
    bottom: 10,
    right: 10,
    background: "rgba(255,255,255,0.92)",
    borderRadius: 8,
    padding: "6px 12px",
    display: "flex",
    gap: 12,
    fontSize: 13,
    fontWeight: 600,
    zIndex: 1000,
    boxShadow: "0 1px 4px rgba(0,0,0,0.15)",
  },
};
