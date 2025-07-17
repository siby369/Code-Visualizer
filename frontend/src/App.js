import React from "react";
import "./App.css";

function App() {
  return (
    <div className="modern-root">
      <nav className="modern-navbar">
        <div className="modern-navbar-left">Code Visualizer</div>
        <div className="modern-navbar-right">
          <button className="modern-nav-btn">Settings</button>
          <button className="modern-nav-btn">Feedback</button>
          <button className="modern-nav-btn">Login</button>
        </div>
      </nav>
      {/* UI content area remains empty as requested */}
    </div>
  );
}

export default App;