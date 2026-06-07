import { useState, useRef } from "react";

export default function RouteForm({ onSubmit, loading }) {
  const [viaList, setViaList] = useState([]);
  const fromRef = useRef();
  const toRef = useRef();
  const departureRef = useRef();

  function addVia() {
    if (viaList.length < 5) setViaList([...viaList, ""]);
  }

  function removeVia(index) {
    setViaList(viaList.filter((_, i) => i !== index));
  }

  function updateVia(index, value) {
    const next = [...viaList];
    next[index] = value;
    setViaList(next);
  }

  function handleSubmit(e) {
    e.preventDefault();
    const departureTime = departureRef.current.value || null;
    onSubmit(fromRef.current.value, toRef.current.value, departureTime, viaList.filter(Boolean));
  }

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h1 style={styles.title}>Weayther</h1>
      <p style={styles.subtitle}>ルート上の天気予報</p>
      <div style={styles.row}>
        <div style={styles.field}>
          <label style={styles.label}>出発地点</label>
          <input ref={fromRef} name="from" required placeholder="例：東京駅" style={styles.input} />
        </div>
        <div style={styles.arrow}>→</div>
        <div style={styles.field}>
          <label style={styles.label}>到着地点</label>
          <input ref={toRef} name="to" required placeholder="例：大阪駅" style={styles.input} />
        </div>
      </div>

      {viaList.length > 0 && (
        <div style={styles.viaSection}>
          <label style={styles.label}>経由地</label>
          {viaList.map((v, i) => (
            <div key={i} style={styles.viaRow}>
              <input
                value={v}
                onChange={(e) => updateVia(i, e.target.value)}
                placeholder={`経由地 ${i + 1}`}
                style={{ ...styles.input, flex: 1 }}
              />
              <button type="button" onClick={() => removeVia(i)} style={styles.removeButton}>
                ✕
              </button>
            </div>
          ))}
        </div>
      )}

      {viaList.length < 5 && (
        <button type="button" onClick={addVia} style={styles.addButton}>
          ＋ 経由地を追加
        </button>
      )}

      <div style={styles.departureSection}>
        <label style={styles.label}>出発時間（任意）</label>
        <input ref={departureRef} type="datetime-local" style={styles.input} />
      </div>

      <button type="submit" disabled={loading} style={styles.button}>
        {loading ? "取得中..." : "天気を調べる"}
      </button>
    </form>
  );
}

const styles = {
  form: {
    background: "#fff",
    borderRadius: 12,
    padding: "32px 40px",
    boxShadow: "0 2px 16px rgba(0,0,0,0.08)",
    maxWidth: 700,
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: 16,
  },
  title: { fontSize: 28, fontWeight: 700, color: "#2b6cb0", marginBottom: 0 },
  subtitle: { color: "#718096", marginTop: 0 },
  row: { display: "flex", gap: 16, alignItems: "flex-end", flexWrap: "wrap" },
  field: { flex: 1, display: "flex", flexDirection: "column", gap: 6, minWidth: 180 },
  label: { fontSize: 13, fontWeight: 600, color: "#4a5568", marginBottom: 4 },
  input: {
    padding: "10px 14px",
    borderRadius: 8,
    border: "1.5px solid #cbd5e0",
    fontSize: 15,
    outline: "none",
    boxSizing: "border-box",
    width: "100%",
  },
  arrow: { fontSize: 24, color: "#a0aec0", paddingBottom: 8 },
  viaSection: { display: "flex", flexDirection: "column", gap: 8 },
  viaRow: { display: "flex", gap: 8, alignItems: "center" },
  addButton: {
    alignSelf: "flex-start",
    padding: "7px 14px",
    borderRadius: 8,
    border: "1.5px dashed #90cdf4",
    background: "#ebf8ff",
    color: "#2b6cb0",
    fontSize: 13,
    fontWeight: 600,
    cursor: "pointer",
  },
  removeButton: {
    padding: "6px 10px",
    borderRadius: 8,
    border: "1px solid #fed7d7",
    background: "#fff5f5",
    color: "#c53030",
    fontSize: 13,
    cursor: "pointer",
    flexShrink: 0,
  },
  departureSection: { display: "flex", flexDirection: "column", gap: 6 },
  button: {
    marginTop: 4,
    width: "100%",
    padding: "12px",
    borderRadius: 8,
    border: "none",
    background: "#2b6cb0",
    color: "#fff",
    fontSize: 16,
    fontWeight: 600,
    cursor: "pointer",
  },
};
