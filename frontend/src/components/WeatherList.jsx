import WeatherCard from "./WeatherCard.jsx";

export default function WeatherList({ waypoints }) {
  if (!waypoints.length) return null;
  const last = waypoints.length - 1;

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>ルート上の天気予報 — {waypoints.length} 地点</h2>
      <div style={styles.list}>
        {waypoints.map((wp, i) => (
          <WeatherCard key={i} data={wp} isFirst={i === 0} isLast={i === last} />
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: { maxWidth: 700, margin: "0 auto" },
  heading: { fontSize: 18, fontWeight: 600, color: "#4a5568", marginBottom: 16 },
  list: { display: "flex", flexDirection: "column", gap: 12 },
};
