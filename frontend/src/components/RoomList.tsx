import { useEffect, useState } from "react";
import axios from "axios";
import { apiBaseUrl, baseAppUrl } from "../App";
import "./RoomList.css";
import copyToClipboard from "./util";

interface RoomListProps {
  userId: number;
}

export const RoomList = (props: RoomListProps) => {
  const [roomList, setRoomList] = useState<Array<string>>([]);

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
          const url = baseAppUrl + "chat/" + roomId + "/" + props.userId;
          return (
            <p className="roomIdItem" key={index}>
              <a>{roomId}</a>
              <button className="button" onClick={() => {
                window.location.href = url;
              }}> Join room
              </button>
              <button className="button" onClick={() => {
                copyToClipboard(roomId);
              }}> copy join code
              </button>
              <button className="button" onClick={() => {
                copyToClipboard(url);
              }}> copy join url for user {props.userId}
              </button>
            </p>
          );
        })}
      </div>

    </div>
  );
};
