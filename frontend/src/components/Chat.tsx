import { FormEvent, useEffect, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import axios from "axios";
import { apiBaseUrl, baseAppUrl } from "../App";
import { RoomList } from "./RoomList";
import "./Chat.css";
import { useParams } from "react-router-dom";
import copyToClipboard from "./util";

export const Chat = () => {
  const [currentMessage, setCurrentMessage] = useState("");
  const [roomCode, setRoomCode] = useState<string>("");
  const [userId, setUserId] = useState<number>(1);
  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const [messageList, setMessageList] = useState<Array<{ data: string }>>([]);
  const [loggedRoomCode, setLoggedRoomCode] = useState<string | null>(null);
  const [loggedUserId, setLoggedUserId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [newRoomPrivacy, setNewRoomPrivacy] = useState<string>("public");
  const params = useParams();


  useEffect(() => {
    if (params.roomId && params.userId) {
      console.log(params);
      console.log(params.roomId);
      console.log(params.userId);
      setRoomCode(params.roomId);
      const paramUserId = parseInt(params.userId);
      setUserId(paramUserId);
      console.log("trying to connect in useEffect");
      joinRoom(params.roomId, paramUserId).then();
    }

  }, []);
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
        params: { user_id: userId, private: (newRoomPrivacy == "private") },
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
    await joinRoom(roomCode, userId);
  };

  const joinRoom = async (joinRoomCode: string, joinRoomUserId: number) => {

    try {
      const response = await axios.get(`${apiBaseUrl}/join-room`, {
        // eslint-disable-next-line camelcase
        params: { room_code: joinRoomCode, user_id: joinRoomUserId },
      });
      if (response.data.room_exists) {
        setSocketUrl(`${apiBaseUrl}/ws/connect/${joinRoomCode}?user_id=${joinRoomUserId}`);
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
        <label htmlFor="visibility-dropdown">Visibility of new room: </label>
        <select
          id="visibility-dropdown"
          value={newRoomPrivacy}
          onChange={(e) => {
            setNewRoomPrivacy(e.target.value);
          }}
        >
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
        <br />
        <button onClick={handleCreateRoom}>Create Room</button>
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
      {(loggedUserId &&
        <div>Logged in as user: {loggedUserId} in room: {loggedRoomCode}</div>)
        ||
        <div>Not logged in </div>
      }
      {error &&
        <div style={{ color: "red" }}>{error}</div>
      }

      {loggedUserId &&
        <button className="button" onClick={() => {
          copyToClipboard(roomCode);
        }}>
          copy room code
        </button>
      }
      {loggedUserId &&
        <button className="button" onClick={() => {
          const url = baseAppUrl + "chat/" + roomCode + "/" + userId;
          copyToClipboard(url);
        }}>
          copy join url for user {userId}
        </button>
      }
      <br />
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
      <RoomList
        userId={userId} />
    </div>
  );
};
