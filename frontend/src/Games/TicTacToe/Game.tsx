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
  const [userId, setUserId] = useState<number | null>(null);
  const { roomCode } = useRoom();
  const { sendRequest, response, resetGameBackend } = useGameBackend(roomCode);
  const [isGameOver, setIsGameOver] = useState<boolean>(false);
  const [gameOverMessage, setGameOverMessage] = useState<string>("");
  const [myTurn, setMyTurn] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const turnMessage = myTurn ? "Your turn" : "Opponent's turn";
  const isGameInProgress = gameState && !isGameOver;


  const handleJoin = () => {
    const request = JSON.stringify({ action: "join" });
    console.log("Requesting to join game with id: ", roomCode);
    sendRequest(request);
  };

  const resetGame = () => {
    setGameState(null);
    setUserId(null);
    setIsGameOver(false);
    setGameOverMessage("");
    setMyTurn(false);
    resetGameBackend();
  };

  useEffect(() => {
    console.log("My turn updated:", myTurn);
  }, [myTurn]);

  useEffect(() => {
    console.log("room code changed to ", roomCode);
    resetGame();
  }, [roomCode]);

  useEffect(() => {
    if (response) {
      setError(null);
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
        const winner = parsedResponse.winner;
        console.log("winner: ", winner);
        const msg = parsedResponse.winner === userId ? "You win!" : (winner == null ? "It's a draw" : "You lose!");
        setGameOverMessage(msg);

      } else if (parsedResponse.action === "error") {
        console.error("Error:", parsedResponse.message);
        setError(parsedResponse.message);
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
      {error && <p>{error}</p>}
      {gameState && <Board board={gameState.board} onClick={handleBoardClick} disabled={!myTurn} />}
      {!isGameInProgress && gameState &&
        <button onClick={resetGame}>Quit game</button>}
    </div >
  );
};
