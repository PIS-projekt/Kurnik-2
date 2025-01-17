import {FormEvent, useEffect, useState} from "react";
import useWebSocket, {ReadyState} from "react-use-websocket";
import axios from "axios";
import {apiBaseUrl, baseAppUrl} from "../App";
import {useNavigate} from "react-router-dom";
import {RoomList} from "./RoomList";
import "./Chat.css";
import {useParams} from "react-router-dom";

import {jwtDecode} from "jwt-decode";

import {useRoom} from "../hooks/useRoom";


export const Chat = () => {
  const [currentMessage, setCurrentMessage] = useState("");
  const {roomCode, setRoomCode} = useRoom();
  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const [messageList, setMessageList] = useState<Array<{ data: string }>>([]);
  const [loggedRoomCode, setLoggedRoomCode] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [newRoomPrivacy, setNewRoomPrivacy] = useState<string>("public");
  const params = useParams();

  const [userName, setUserName] = useState<string | null>(null);

  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    if (!token) {
      navigate("/login");
      return;
    }

    try {
      const decodedToken: { sub: string; exp: number } = jwtDecode(token);
      setUserName(decodedToken.sub);

      // Check if the token is expired
      if (decodedToken.exp * 1000 < Date.now()) {
        handleLogout();
        return;
      }
    } catch (error) {
      console.error("Invalid token:", error);
      handleLogout();
    }
    const joinRoomId = params.roomId?.toString();
    if (joinRoomId){
      joinRoom(joinRoomId);
    }
  }, [navigate]);

  useEffect(() => {
    if (userName) {
      console.log("User name:", userName);
    }
  }, [userName]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  useEffect(() => {
    if (params.roomId && params.userId) {
      console.log(params);
      console.log(params.roomId);
      console.log("trying to connect in useEffect");
      joinRoom(params.roomId).then();
    }

  }, []);
  const handleOpen = () => {
    console.log("WebSocket connection opened.");
    setLoggedRoomCode(roomCode);
    setError(null);
  };

  const handleClose = () => {
    console.log("WebSocket connection closed.");
    setMessageList([]);
    setLoggedRoomCode(null);
  };

  const handleMessage = (message: { data: string }) => {
    setMessageList((prevMessages) => [...prevMessages, message]);
  };

  const {sendMessage, readyState} = useWebSocket(socketUrl, {
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
      const token = localStorage.getItem("access_token");
      const response = await axios.get(`${apiBaseUrl}/create-new-room`, {
        params: {private: (newRoomPrivacy == "private")},
        headers: {Authorization: `Bearer ${token}`},

      });
      const newRoomCode = response.data.room_code;
      setRoomCode(newRoomCode);
      navigate("/chat/" + newRoomCode);
      setSocketUrl(`${apiBaseUrl}/ws/connect/${newRoomCode}?token=${token}`);
      setError("Room created and joined successfully.");
    } catch (error) {
      console.error("Failed to create room:", error);
      setError("Failed to create room. Please try again.");
    }
  };

  const handleJoinRoom = async (event: FormEvent) => {
    event.preventDefault();
    navigate("/chat/" + roomCode);
  };

  const joinRoom = async (joinRoomCode: string) => {

    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(`${apiBaseUrl}/join-room`, {
        // eslint-disable-next-line camelcase
        params: {room_code: joinRoomCode},
        headers: {Authorization: `Bearer ${token}`},
      });
      if (response.data.room_exists) {
        setSocketUrl(`${apiBaseUrl}/ws/connect/${joinRoomCode}?token=${token}`);
        setRoomCode(joinRoomCode);
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
      <br/>
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
        <br/>
        <button onClick={handleCreateRoom}>Create Room</button>
      </div>
      <br/>
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
      <br/>
      <div>Logged in as user: {userName} in room: {loggedRoomCode}</div>
      {error &&
          <div style={{color: "red"}}>{error}</div>
      }


      <button className="button" onClick={() => {
        navigator.clipboard.writeText(roomCode);
      }}>
        copy room code
      </button>
      <button className="button" onClick={() => {
        const url = baseAppUrl + "chat/" + roomCode + "/" + 1;
        navigator.clipboard.writeText(url);
      }}>
        copy join url for user {}
      </button>
      <br/>
      <br/>
      <div>
        <button onClick={handleLogout}>Logout</button>
      </div>
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
          <p className="messageListItem" key={index}>
            {message.data}
          </p>
        ))}
      </div>
      <RoomList userId={1}/>
    </div>
  );
};
