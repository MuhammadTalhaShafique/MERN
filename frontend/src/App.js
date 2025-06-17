import React, { useState } from "react";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Notes from "./components/Notes";
import "./App.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [showSignup, setShowSignup] = useState(false);

  const handleLogin = (token) => {
    localStorage.setItem("token", token);
    setToken(token);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <div>
      {!token ? (
        showSignup ? (
          <Signup
            onSignup={handleLogin}
            showLogin={() => setShowSignup(false)}
          />
        ) : (
          <Login onLogin={handleLogin} showSignup={() => setShowSignup(true)} />
        )
      ) : (
        <Notes token={token} onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;
