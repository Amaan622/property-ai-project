import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";

import Header from "./component/Header";
import Help from "./pages/Help";
import Contact from "./pages/Contact";

function App() {
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_URL = "https://property-ai-project.onrender.com";

  const handleSearch = async () => {
    if (!query.trim()) return;

    setChat((prev) => [...prev, { type: "user", text: query }]);
    setLoading(true);

    const currentQuery = query;
    setQuery("");

    try {
      const res = await fetch(`${API_URL}/property/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: currentQuery })
      });

      const data = await res.json();

      setResults(data.results || []);

      setChat((prev) => [
        ...prev,
        { type: "bot", text: data.message || "Response received" }
      ]);

    } catch (err) {
      console.error(err);

      setChat((prev) => [
        ...prev,
        { type: "bot", text: "❌ Server error. Please check backend." }
      ]);

      setResults([]);
    }

    setLoading(false);
  };

  const getTagClass = (tag) => {
    if (!tag) return "tag-normal";

    const t = tag.toLowerCase();

    if (t.includes("good")) return "tag-good";
    if (t.includes("consider")) return "tag-consider";
    if (t.includes("bad") || t.includes("reject")) return "tag-bad";

    return "tag-normal";
  };

  return (
    <Router>
      <div className="page-container">

        <Header />

        <Routes>

          {/* HOME */}
          <Route
            path="/"
            element={
              <div className="chat-wrapper">

                {/* CHAT BOX */}
                <div className="chat-box">
                  {chat.map((msg, i) => (
                    <div
                      key={i}
                      className={msg.type === "user" ? "user-msg" : "bot-msg"}
                    >
                      {msg.text}
                    </div>
                  ))}
                </div>

                {/* INPUT */}
                <div className="input-box">
                  <input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Try: Budget 3 BHK in Sarhapur"
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  />

                  <button onClick={handleSearch}>
                    {loading ? "Searching..." : "Ask AI"}
                  </button>
                </div>

                {/* RESULTS */}
                <div className="results-grid">
                  {results.map((item, index) => (
                    <div
                      key={index}
                      className={`card ${item.score >= 80 ? "good" : "normal"}`}
                    >
                      <h3 className="location">{item.location}</h3>

                      <div className="meta">
                        <span>🏢 {item.bhk} BHK</span>
                        <span>💰 ₹{item.price} Lakh</span>
                        <span>⭐ {item.score}</span>
                      </div>

                      <span className={getTagClass(item.tag)}>
                        {item.tag}
                      </span>

                      <p className="why">
                        <b>Why:</b>{" "}
                        {Array.isArray(item.explanation)
                          ? item.explanation.join(", ")
                          : item.explanation}
                      </p>

                      <p className="insight">
                        <b>Insight:</b> {item.market_insight}
                      </p>
                    </div>
                  ))}
                </div>

              </div>
            }
          />

          <Route path="/help" element={<Help />} />
          <Route path="/contact" element={<Contact />} />

        </Routes>

        {/* FOOTER */}
        <footer className="footer">
          <div className="footer-content">

            <p>🏡 Property AI - Smart Recommendation System</p>

            <p>
              Built with React ⚛️ + Flask 🐍 | Deployed on Vercel & Render ☁️
            </p>

            <p className="footer-links">
              <a
                href="https://property-ai-project.vercel.app"
                target="_blank"
                rel="noreferrer"
              >
                Live App
              </a>
              {" | "}
              <a
                href="https://github.com/Amaan622/property-ai-project"
                target="_blank"
                rel="noreferrer"
              >
                GitHub
              </a>
            </p>

            <p className="copyright">
              © {new Date().getFullYear()} Amaan. All rights reserved.
            </p>

          </div>
        </footer>

      </div>
    </Router>
  );
}

export default App;