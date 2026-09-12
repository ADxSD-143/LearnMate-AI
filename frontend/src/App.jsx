import { useState } from "react";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function App() {
  const [health, setHealth] = useState("Not checked");

  async function checkHealth() {
    setHealth("Checking...");
    try {
      const response = await fetch(`${apiBaseUrl}/health/`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      setHealth(data.status || "Healthy");
    } catch (error) {
      setHealth(`Unavailable: ${error.message}`);
    }
  }

  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">LearnMate AI</p>
        <h1>Your learning system, in one place.</h1>
        <p className="lede">
          Track subjects, attendance, quizzes, recommendations, and study plans
          from the LearnMate backend.
        </p>
        <div className="actions">
          <button type="button" onClick={checkHealth}>
            Check backend
          </button>
          <a href={`${apiBaseUrl}/docs`} target="_blank" rel="noreferrer">
            Open API docs
          </a>
        </div>
        <p className="status" aria-live="polite">
          Backend status: {health}
        </p>
      </section>
    </main>
  );
}
