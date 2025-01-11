import useWebSocket from "react-use-websocket";
import {useState} from "react";

export const useGameBackend = (sessionId: string, userId: number) => {
  const [response, setResponse] = useState<string | null>(null);
  const [socketUrl, setSocketUrl] = useState<string | null>(null);

  const apiBaseUrl = "ws://localhost:8000";
  const apiUrl = `${apiBaseUrl}/tictactoe/game/${sessionId}?user_id=${userId}`;

  const handleOpen = () => console.log("WebSocket connection opened.");

  const handleClose = () => console.log("WebSocket connection closed.");

  const handleMessage = (message: { data: string }) => {
    const msg = message.data as string;
    setResponse(msg);
    // setSocketUrl(null);
  };

  const {sendMessage} = useWebSocket(socketUrl, {
    onOpen: handleOpen,
    onClose: handleClose,
    onMessage: handleMessage,
    shouldReconnect: () => false,
  });

  const sendRequest = (message: string) => {
    setSocketUrl(apiUrl);
    sendMessage(message);
  };

  return {sendRequest: sendRequest, response: response};
};