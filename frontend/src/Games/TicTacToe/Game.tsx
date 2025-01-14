import { useEffect, useState } from "react";
import { useGameBackend } from "./useGameBackend";
import { Board } from "./Board";
import { useRoom } from "../../hooks/useRoom";

interface GameState {
  board: string[][];
  turn: number;
}


export const Game = () => {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [userId, setUserId] = useState<number>(1);
  const { roomCode } = useRoom();
  const [sessionId, setSessionId] = useState<string>(roomCode);
  const { sendRequest, response } = useGameBackend(sessionId, userId);
  const [isGameOver, setIsGameOver] = useState<boolean>(false);
  const [gameOverMessage, setGameOverMessage] = useState<string>("");
  const [myTurn, setMyTurn] = useState<boolean>(false);

  const turnMessage = myTurn ? "Your turn" : "Opponent's turn";
  const isGameInProgress = gameState && !isGameOver;


  const handleJoin = () => {
    const request = JSON.stringify({ action: "join" });
    console.log("Requesting to join game with id: ", sessionId);
    sendRequest(request);
  };

  useEffect(() => {
    console.log("My turn updated:", myTurn);
  }, [myTurn]);

  useEffect(() => {
    console.log("room code changed to ", roomCode);
    setSessionId(roomCode);
  }, [roomCode]);

  useEffect(() => {
    if (response) {
      const parsedResponse = JSON.parse(response);
      console.info("Received response:", parsedResponse);

      if (parsedResponse.action === "accept_join") {
        setGameState(parsedResponse.state);
        setUserId(parsedResponse.user_id);
        setMyTurn(parsedResponse.state.turn === parsedResponse.user_id);
        console.log("My turn:", parsedResponse.state.turn === parsedResponse.user_id);

      } else if (parsedResponse.action === "update_state") {
        setGameState(parsedResponse.state);
        setMyTurn(parsedResponse.state.turn === userId);

      } else if (parsedResponse.action === "game_over") {
        setGameState(parsedResponse.state);
        setIsGameOver(true);
        const msg = parsedResponse.winner === userId ? "You win!" : "You lose!";
        setGameOverMessage(msg);
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
      <button onClick={handleJoin}>Join</button>
      <p>{isGameInProgress && turnMessage}</p>
      <p>{gameOverMessage}</p>
      {gameState && <Board board={gameState.board} onClick={handleBoardClick} disabled={!myTurn} />}
    </div>
  );
};
