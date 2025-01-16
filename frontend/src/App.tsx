import "./App.css";
import { Chat } from "./components/Chat";
import { ChatComp } from "./components/ChatComp";
import RoomCreateJoin from "./components/RoomCreateJoin";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { Login } from "./components/Login";
import { Register } from "./components/Register";
import { Game } from "./Games/TicTacToe/Game";
import { RoomContextProvider } from "./hooks/useRoom";
import Navbar from "./components/Navbar";
import GamePage from "./components/GamePage";
import { useUser } from "./hooks/useUser";

function App() {
  const { isAuthenticated } = useUser();

  return (
    <Router>

      <Navbar />
      <Routes>
        <Route
          path="/"
          element={isAuthenticated ? <Navigate to="/chat" /> : <Navigate to="/login" />}
        />
        <Route
          path="/chat"
          element={isAuthenticated ? <RoomContextProvider><GamePage /></RoomContextProvider> : <Navigate to="/login" />}
        />
        <Route
          path="/login"
          element={<Login />}
        />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;
