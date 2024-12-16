import {useState, FormEvent} from "react";
import useWebSocket from "react-use-websocket";


export const Chat = () => {
  const [count, setCount] = useState(0);
  const [currentMessage, setCurrentMessage] = useState("");
  const [roomId, setRoomId] = useState<number>(1);
  const [userId, setUserId] = useState<number>(1);
  const [socketUrl, setSocketUrl] = useState<string | null>(null);


  const apiUrl = "localhost:8000/ws/";
  const handleOpen = () => console.log("WebSocket connection opened.");
  const handleClose = () => console.log("WebSocket connection closed.");

  const handleMessage = (message: { data: string }) => {

    const msg = message.data as string;
    if (msg.startsWith("Close connection")) {
      setSocketUrl(null);
    }
  };

  // The sockets url will change when the socketUrl changes. it will establish a new connection
  const {sendMessage} = useWebSocket(socketUrl, {
    onOpen: handleOpen,
    onClose: handleClose,
    onMessage: handleMessage,
    shouldReconnect: () => true,
  });

  const handleSendMessage = () => {
    sendMessage(currentMessage);
    setCurrentMessage("");

  };


  const handleJoinRoom = (event:FormEvent) => {
    event.preventDefault();
    setSocketUrl(apiUrl + roomId + "?user_id=" + userId);
  };


  return (
    <div className="Chatroom">
      <h1>Chatroom</h1>
      <form action=""
        onSubmit={(event) => handleJoinRoom(event)}>
        <label htmlFor="room">Room Name:</label>
        <input
          type="text"
          value={roomId}
          onChange={(e) => setRoomId(parseInt(e.target.value))}
          required
        />
        <label htmlFor="user_id">User ID:</label>
        <input
          type="text"
          id="user_id"
          value={userId}
          onChange={(e) => setUserId(parseInt(e.target.value))}
          required
        />
        <button>Join Room</button>
      </form>
      <div id="chat"></div>
      <input type="text"
        id="message"
        placeholder="Type your message here..."
        value={currentMessage}
        onChange={(e) => setCurrentMessage(e.target.value)}/>
      <button onClick={(() => handleSendMessage())}>Send Message</button>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </div>
  );
};