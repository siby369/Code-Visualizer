<<<<<<< HEAD
import React from "react";
import "./App.css";

function App() {
=======
import React, { useState } from "react";
import "./App.css";

function AuthModal({ open, onClose }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  if (!open) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const endpoint = mode === "login" ? "http://localhost:8000/login" : "http://localhost:8000/signup";
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    setMsg(data.message || data.detail || "");
    if (res.ok && mode === "login") onClose();
  };

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <button onClick={onClose} style={{ float: "right" }}>X</button>
        <h2>{mode === "login" ? "Login" : "Sign Up"}</h2>
        <form onSubmit={handleSubmit}>
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
          <button type="submit">{mode === "login" ? "Login" : "Sign Up"}</button>
        </form>
        <p>{msg}</p>
        <button onClick={() => setMode(mode === "login" ? "signup" : "login")}
          style={{ marginTop: "1rem" }}>
          {mode === "login" ? "Go to Sign Up" : "Go to Login"}
        </button>
      </div>
    </div>
  );
}

function App() {
  const [authOpen, setAuthOpen] = useState(false);
>>>>>>> 4e063f6 (login database)
  return (
    <div className="modern-root">
      <nav className="modern-navbar">
        <div className="modern-navbar-left">Code Visualizer</div>
        <div className="modern-navbar-right">
          <button className="modern-nav-btn">Settings</button>
          <button className="modern-nav-btn">Feedback</button>
<<<<<<< HEAD
          <button className="modern-nav-btn">Login</button>
        </div>
      </nav>
      {/* UI content area remains empty as requested */}
=======
          <button className="modern-nav-btn" onClick={() => setAuthOpen(true)}>Login</button>
        </div>
      </nav>
      {/* UI content area remains empty as requested */}
      <AuthModal open={authOpen} onClose={() => setAuthOpen(false)} />
>>>>>>> 4e063f6 (login database)
    </div>
  );
}

export default App;