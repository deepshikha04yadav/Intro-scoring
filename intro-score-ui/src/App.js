import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [duration, setDuration] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!text || !duration) {
      alert("Please enter transcript and duration.");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/score", {
        text,
        duration_sec: Number(duration),
      });
      setResult(res.data);
    } catch (err) {
      alert("Error connecting to backend");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h2>🎤 Spoken Introduction Scoring</h2>

      <textarea
        rows="8"
        placeholder="Enter spoken transcript..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <input
        type="number"
        placeholder="Duration in seconds"
        value={duration}
        onChange={(e) => setDuration(e.target.value)}
      />

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Scoring..." : "Evaluate"}
      </button>

      {result && (
        <div className="result-box">
          <h3>Final Score: {result.final_score_0_100}/100</h3>

          <h4>Breakdown</h4>
          {result.criteria.map((c, i) => (
            <div key={i} className="criterion">
              <strong>{c.name}</strong> — {c.raw_score}/{c.max_score}  
              <details>
                <summary>Details</summary>
                <pre>{JSON.stringify(c.details, null, 2)}</pre>
              </details>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
