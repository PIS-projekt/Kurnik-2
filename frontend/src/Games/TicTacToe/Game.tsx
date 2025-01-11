import {useEffect, useState} from "react";
import {useGameBackend} from "./useGameBackend";
import {Board} from "./Board";

interface GameState {
  board: string[][];
  turn: number;
}

const initialBoard = [["", "", ""], ["", "", ""], ["", "", ""]];

export const Game = () => {
  const [gameState, setGameState] = useState<GameState>({ board: initialBoard, turn: 1 });
  const [userId, setUserId] = useState<number>(1);
  const [sessionId, setSessionId] = useState<string>("abc");
  const { sendRequest, response } = useGameBackend(sessionId, userId);

  const handleClick = () => {
    const request = JSON.stringify({ action: "press_button" });
    sendRequest(request);
  };

  const handleJoin = () => {
    const request = JSON.stringify({ action: "join" });
    sendRequest(request);
  };

  useEffect(() => {
    if (response) {
      const parsedResponse = JSON.parse(response);
      console.info("Received response:", parsedResponse);

      if (parsedResponse.action === "update_state") {
        setGameState(parsedResponse.state);
      }
    }
  }, [response]);

  const handleBoardClick = (x: number, y: number) => {
    const request = JSON.stringify({ action: "place_mark", x: x, y: y });
    sendRequest(request);
  };

  return (
    <div>
      <h1>Game</h1>
      <input type="number" value={userId} onChange={(e) => setUserId(parseInt(e.target.value))}/>
      <input type="text" value={sessionId} onChange={(e) => setSessionId(e.target.value)}/>
      <button onClick={handleJoin}>Join</button>
      <button onClick={handleClick} disabled={gameState.turn !== userId}>Press</button>
      <p>Turn: {gameState.turn}</p>
      <Board board={gameState.board} onClick={handleBoardClick} />
    </div>
  );
};