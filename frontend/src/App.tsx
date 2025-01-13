import "./App.css";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { Chat } from "./components/Chat";
import { Login } from "./components/Login";
import { Register } from "./components/Register";
import {Game} from "./Games/TicTacToe/Game";
import {RoomContextProvider} from "./hooks/useRoom";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check for token in localStorage to determine authentication status
    const token = localStorage.getItem("access_token");
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <Router>
      <div className="App">
        <h1>Projekt PIS 2024Z</h1>
        <p>Profile: {process.env.NODE_ENV}</p>

        <Routes>
          {/* Redirect to chat if authenticated, otherwise go to login */}
          <Route
            path="/"
            element={isAuthenticated ? <Navigate to="/chat" /> : <Navigate to="/login" />}
          />
          <Route
            path="/chat"
            element={isAuthenticated ?   <RoomContextProvider><Chat/><Game/></RoomContextProvider> : <Navigate to="/login" />}
          />
          <Route
            path="/login"
            element={<Login setIsAuthenticated={setIsAuthenticated} />}
          />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
