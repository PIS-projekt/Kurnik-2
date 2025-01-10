import "./App.css";
import { Chat } from "./components/Chat";
import { BrowserRouter, Routes, Route } from "react-router-dom";

export const apiBaseUrl = "http://0.0.0.0:8000";
export const baseAppUrl = "http://localhost:3000/";

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path={"chat/:roomId/:userId"} element={<Chat />} />
        <Route path="/" element={
          <div className="App">
            <h1>Projekt PIS 2024Z</h1>
            <p>Profile: {process.env.NODE_ENV}</p>
            <Chat />
          </div>}>
        </Route>

      </Routes>

    </BrowserRouter>

  );
}

export default App;
