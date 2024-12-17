import {FormEvent, useState} from "react";
import useWebSocket, {ReadyState} from "react-use-websocket";


export const Chat = () => {
  const [currentMessage, setCurrentMessage] = useState("");
  const [selectedRoomId, setSelectedRoomId] = useState<number>(1);
  const [userId, setUserId] = useState<number>(1);
  const [socketUrl, setSocketUrl] = useState<string | null>(null);
  const [messageList, setMessageList] = useState<Array<{ data: string }>>([]);
  const [loggedRoomId, setLoggedRoomId] = useState<number|null>(null);
  const [loggedUserId, setLoggedUserId] = useState<number|null>(null);

  const apiUrl = "http://localhost:8000/ws/";
  const handleOpen = () => {
    console.log("WebSocket connection opened.");
    setLoggedRoomId(selectedRoomId);
    setLoggedUserId(userId);
  };
  const handleClose = () => {
    console.log("WebSocket connection closed.");
    setMessageList([]);
    setLoggedRoomId(null);
    setLoggedUserId(null);
  };

  const handleMessage = (message: { data: string }) => {
    console.log(messageList);
    messageList.push(message);
    setMessageList(messageList);
    const msg = message.data as string;
    if (msg.startsWith("Close connection")) {
      setSocketUrl(null);
    }

  };

  // The sockets url will change when the socketUrl changes. it will establish a new connection
  const {sendMessage, readyState} = useWebSocket(socketUrl, {
    onOpen: handleOpen,
    onClose: handleClose,
    onMessage: handleMessage,
    shouldReconnect: () => true,
  });

  const handleSendMessage = () => {
    if (currentMessage && readyState == ReadyState.OPEN){
      sendMessage(currentMessage);
      setCurrentMessage("");
    }

  };


  const handleJoinRoom = (event: FormEvent) => {
    event.preventDefault();
    setSocketUrl(apiUrl + selectedRoomId + "?user_id=" + userId);
  };


  return (
    <div className="Chatroom">
      <h1>Chatroom</h1>
      <form action=""
        onSubmit={(event) => handleJoinRoom(event)}>
        <label htmlFor="room">Room Name:</label>
        <input
          type="number"
          value={selectedRoomId}
          onChange={(e) => setSelectedRoomId(parseInt(e.target.value))}
          required
        />
        <label htmlFor="user_id">User ID:</label>
        <input
          type="number"
          id="user_id"
          value={userId}
          onChange={(e) => setUserId(parseInt(e.target.value))}
          required
        />
        <button>Join Room</button>
      </form>
      <div> Logged in as user: {loggedUserId} in room {loggedRoomId} </div>
      <div id="chat"></div>
      <input type="text"
        id="message"
        placeholder="Type your message here..."
        value={currentMessage}
        onChange={(e) => setCurrentMessage(e.target.value)}/>
      <button onClick={(() => handleSendMessage())}>Send Message
      </button>
      <div id="Chat">
        {messageList.map( message => <p className="skibido" key={message.data.length}>{message.data}</p>)}
      </div>
    </div>
  );
};