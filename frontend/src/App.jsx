import { useState } from "react";
import RouteForm from "./components/RouteForm.jsx";
import MapView from "./components/MapView.jsx";
import WeatherList from "./components/WeatherList.jsx";
import { fetchWeatherRoute } from "./api/client.js";

export default function App() {
  const [waypoints, setWaypoints] = useState([]);
  const [route, setRoute] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(from_, to_, departureTime, via) {
    setLoading(true);
    setError(null);
    setWaypoints([]);
    setRoute([]);
    try {
      const data = await fetchWeatherRoute(from_, to_, departureTime, via);
      setWaypoints(data.waypoints);
      setRoute(data.route);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.page}>
      <RouteForm onSubmit={handleSubmit} loading={loading} />
      {error && <div style={styles.error}>{error}</div>}
      {waypoints.length > 0 && (
        <>
          <MapView waypoints={waypoints} route={route} />
          <WeatherList waypoints={waypoints} />
        </>
      )}
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    padding: "32px 20px",
    maxWidth: 860,
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: 28,
  },
  error: {
    background: "#fff5f5",
    color: "#c53030",
    border: "1px solid #feb2b2",
    borderRadius: 8,
    padding: "12px 16px",
    fontSize: 14,
  },
};
