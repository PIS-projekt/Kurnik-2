import "./App.css";
import { Chat } from "./components/Chat";
import ChatComp from "./components/ChatComp";
import { Game } from "./Games/TicTacToe/Game";
import { RoomContextProvider } from "./hooks/useRoom";

function App() {
  return (
    <RoomContextProvider>
      <div className="App">
        <h1>Projekt PIS 2024Z</h1>
        <p>Profile: {process.env.NODE_ENV}</p>
        <Chat />
        <Game />
        <ChatComp />
      </div>
    </RoomContextProvider>

  );
}

export default App;
