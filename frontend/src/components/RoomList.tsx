import {useEffect, useState} from "react";
import axios from "axios";
import {apiBaseUrl} from "../App";
import "./RoomList.css";
import {useNavigate} from "react-router-dom";

interface RoomListProps {
  userId: number;
}

export const RoomList = (props: RoomListProps) => {
export const RoomList = () => {
  const [roomList, setRoomList] = useState<Array<string>>([]);
  const navigate = useNavigate();

  const handleRefresh = async () => {
    try {
      const response = await axios.get(`${apiBaseUrl}/get-public-rooms`, {});
      setRoomList(response.data["rooms"]);
    } catch (error) {
      console.error("Failed to get rooms:", error);
    }
  };

  useEffect(() => {
    handleRefresh();
  }, []);

  return (
    <div className="RoomLister">
      <div className="RoomList">

        <h2>Public rooms: </h2>
        <button onClick={handleRefresh}>Refresh</button>

        {roomList.map((roomId, index) => {
          return (
            <p className="roomIdItem" key={index}>
              <a>{roomId}</a>
              <button className="button" onClick={() => {
                navigate("/" + "chat/" + roomId);
              }}> Join room
              </button>
              <button className="button" onClick={() => {
                navigator.clipboard.writeText(roomId);
              }}> copy join code
              </button>
              <button className="button" onClick={() => {
                navigator.clipboard.writeText(url);
              }}> copy join url for user {props.userId}
              </button>
            </p>
          );
        })}
      </div>

    </div>
  );
};