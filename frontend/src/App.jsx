import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";

import Header from "./components/Header";
import Help from "./pages/Help";
import Contact from "./pages/Contact";

function App() {
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setChat((prev) => [...prev, { type: "user", text: query }]);
    setLoading(true);

    const currentQuery = query;
    setQuery("");

    try {
      const res = await fetch("http://127.0.0.1:5000/property/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: currentQuery })
      });

      const data = await res.json();

      const properties = data.results || [];
      setResults(properties);

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
                    placeholder="Try: 2 BHK in Whitefield under 1 crore"
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  />

                  <button onClick={handleSearch}>
                    {loading ? "Searching..." : "Ask AI"}
                  </button>
                </div>

                {/* RESULTS */}
                <div className="results-grid">
                  {results.map((item, index) => (
                    <div key={index} className={`card ${item.score >= 80 ? "good" : "normal"}`}>

                      <h3 className="location">{item.location}</h3>

                      <div className="meta">
                        <span>🏢 {item.bhk} BHK</span>
                        <span>💰 ₹{item.price} Lakh</span>
                        <span>⭐ {item.score}</span>
                      </div>

                      {/* TAG */}
                      <span className={getTagClass(item.tag)}>
                        {item.tag}
                      </span>

                      <p className="why"><b>Why:</b> {item.explanation}</p>
                      <p className="insight"><b>Insight:</b> {item.market_insight}</p>
                    </div>
                  ))}
                </div>

              </div>
            }
          />

          <Route path="/help" element={<Help />} />
          <Route path="/contact" element={<Contact />} />

        </Routes>

      </div>
    </Router>
  );
}

export default App;