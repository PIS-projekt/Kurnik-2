import "./App.css";
import { Chat } from "./components/Chat";
import { ChatComp } from "./components/ChatComp";
import RoomCreateJoin from "./components/RoomCreateJoin";
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
        <RoomCreateJoin />
        <ChatComp className="bottom-0 fixed right-0 max-w-[25vw]" />
      </div>
    </RoomContextProvider>

  );
}

export default App;
