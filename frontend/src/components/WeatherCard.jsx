export default function WeatherCard({ data, isFirst, isLast }) {
  const label = isFirst ? "出発" : isLast ? "到着" : `通過点 ${data.index}`;
  const [date, hour] = data.timestamp.split(":");
  const timeLabel = `${date} ${hour}:00`;

  return (
    <div style={{ ...styles.card, borderLeft: `4px solid ${isFirst ? "#48bb78" : isLast ? "#f56565" : "#63b3ed"}` }}>
      <div style={styles.header}>
        <span style={styles.badge}>{label}</span>
        <span style={styles.time}>{timeLabel}</span>
      </div>
      <div style={styles.address}>{data.address}</div>
      <div style={styles.weather}>
        {data.temp != null && (
          <span style={styles.stat}>🌡 {data.temp}°C</span>
        )}
        {data.wind_spd != null && (
          <span style={styles.stat}>💨 {data.wind_spd} m/s</span>
        )}
        <span style={styles.condition}>{data.condition}</span>
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: "#fff",
    borderRadius: 10,
    padding: "16px 20px",
    boxShadow: "0 1px 6px rgba(0,0,0,0.07)",
  },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 },
  badge: {
    fontSize: 12,
    fontWeight: 700,
    background: "#ebf8ff",
    color: "#2b6cb0",
    padding: "2px 8px",
    borderRadius: 12,
  },
  time: { fontSize: 13, color: "#718096" },
  address: { fontSize: 16, fontWeight: 600, marginBottom: 8, color: "#2d3748" },
  weather: { display: "flex", gap: 16, flexWrap: "wrap", alignItems: "center" },
  stat: { fontSize: 14, color: "#4a5568" },
  condition: { fontSize: 13, color: "#718096", fontStyle: "italic" },
};
