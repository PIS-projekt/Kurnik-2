import {useEffect, useState} from "react";
import {useGameBackend} from "./useGameBackend";
import {Board} from "./Board";

interface GameState {
  board: string[][];
  turn: number;
}


export const Game = () => {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [userId, setUserId] = useState<number>(1);
  const [sessionId, setSessionId] = useState<string>("abc");
  const {sendRequest, response} = useGameBackend(sessionId, userId);
  const [isGameOver, setIsGameOver] = useState<boolean>(false);
  const [gameOverMessage, setGameOverMessage] = useState<string>("");

  const myTurn = gameState?.turn === userId && !isGameOver;
  const turnMessage = myTurn ? "Your turn" : "Opponent's turn";
  const isGameInProgress = gameState && !isGameOver;


  const handleJoin = () => {
    const request = JSON.stringify({action: "join"});
    sendRequest(request);
  };

  useEffect(() => {
    if (response) {
      const parsedResponse = JSON.parse(response);
      console.info("Received response:", parsedResponse);

      if (parsedResponse.action === "update_state" || parsedResponse.action === "accept_join") {
        setGameState(parsedResponse.state);
      } else if (parsedResponse.action === "game_over") {
        setGameState(parsedResponse.state);
        setIsGameOver(true);
        const msg = parsedResponse.winner === userId ? "You win!" : "You lose!";
        setGameOverMessage(msg);
      }

    }
  }, [response]);

  const handleBoardClick = (x: number, y: number) => {
    const request = JSON.stringify({action: "place_mark", x: x, y: y});
    sendRequest(request);
  };

  return (
    <div>
      <h1>Game</h1>
      <input type="number" value={userId} onChange={(e) => setUserId(parseInt(e.target.value))}/>
      <input type="text" value={sessionId} onChange={(e) => setSessionId(e.target.value)}/>
      <button onClick={handleJoin}>Join</button>
      <p>{isGameInProgress && turnMessage}</p>
      <p>{gameOverMessage}</p>
      {gameState && <Board board={gameState.board} onClick={handleBoardClick} disabled={!myTurn}/>}
    </div>
  );
};