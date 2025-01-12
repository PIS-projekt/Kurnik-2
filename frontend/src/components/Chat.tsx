import { FormEvent, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import axios from "axios";
import { useRoom } from "../hooks/useRoom";
import { Button } from "./ui/button";

export const Chat = () => {
  const [currentMessage, setCurrentMessage] = useState("");
  const { roomCode, setRoomCode } = useRoom();
  const [userId, setUserId] = useState<number>(1);
  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const [messageList, setMessageList] = useState<Array<{ data: string }>>([]);
  const [loggedRoomCode, setLoggedRoomCode] = useState<string | null>(null);
  const [loggedUserId, setLoggedUserId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const apiBaseUrl = "http://0.0.0.0:8000";

  const handleOpen = () => {
    console.log("WebSocket connection opened.");
    setLoggedRoomCode(roomCode);
    setLoggedUserId(userId);
    setError(null);
  };

  const handleClose = () => {
    console.log("WebSocket connection closed.");
    setMessageList([]);
    setLoggedRoomCode(null);
    setLoggedUserId(null);
  };

  const handleMessage = (message: { data: string }) => {
    setMessageList((prevMessages) => [...prevMessages, message]);
  };

  const { sendMessage, readyState } = useWebSocket(socketUrl, {
    onOpen: handleOpen,
    onClose: handleClose,
    onMessage: handleMessage,
    shouldReconnect: () => true,
  });

  const handleSendMessage = () => {
    if (currentMessage && readyState === ReadyState.OPEN) {
      sendMessage(currentMessage);
      setCurrentMessage("");
    }
  };

  const handleCreateRoom = async () => {
    try {
      const response = await axios.get(`${apiBaseUrl}/create-new-room`, {
        // eslint-disable-next-line camelcase
        params: { user_id: userId, private: false }, // TODO: get setting from user
      });
      const newRoomCode = response.data.room_code;
      setRoomCode(newRoomCode);
      setSocketUrl(`${apiBaseUrl}/ws/connect/${newRoomCode}?user_id=${userId}`);
      setError("Room created and joined successfully.");
    } catch (error) {
      console.error("Failed to create room:", error);
      setError("Failed to create room. Please try again.");
    }
  };

  const handleJoinRoom = async (event: FormEvent) => {
    event.preventDefault();
    try {
      const response = await axios.get(`${apiBaseUrl}/join-room`, {
        // eslint-disable-next-line camelcase
        params: { room_code: roomCode, user_id: userId },
      });
      if (response.data.room_exists) {
        setSocketUrl(`${apiBaseUrl}/ws/connect/${roomCode}?user_id=${userId}`);
        setError("Joined room successfully.");
      }
    } catch (error) {
      console.error("Failed to join room:", error);
      setError("Room not found. Please check the room code.");
    }
  };

  return (
    <div className="Chatroom">
      <h1>Chatroom</h1>
      <div>
        <label htmlFor="user_id">User ID:</label>
        <input
          type="number"
          id="user_id"
          value={userId}
          onChange={(e) => setUserId(parseInt(e.target.value))}
          required
        />
      </div>
      <br />
      <div>
        <Button onClick={handleCreateRoom}>Create Room</Button>
        {/* <button onClick={handleCreateRoom}>Create Room</button> */}
      </div>
      <br />
      <form onSubmit={handleJoinRoom}>
        <label htmlFor="room_code">Room Code:</label>
        <input
          type="text"
          id="room_code"
          value={roomCode}
          onChange={(e) => setRoomCode(e.target.value)}
          required
        />
        <button type="submit">Join Room</button>
      </form>
      <br />
      <div>Logged in as user: {loggedUserId} in room: {loggedRoomCode}</div>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <br />
      <div id="chat"></div>
      <input
        type="text"
        id="message"
        placeholder="Type your message here..."
        value={currentMessage}
        onChange={(e) => setCurrentMessage(e.target.value)}
      />
      <button onClick={handleSendMessage}>Send Message</button>
      <div id="Chat">
        {messageList.map((message, index) => (
          <p className="skibido" key={index}>
            {message.data}
          </p>
        ))}
      </div>
    </div>
  );
};
