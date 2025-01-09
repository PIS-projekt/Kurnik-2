import {useEffect, useState} from "react";
import axios from "axios";
import {apiBaseUrl, baseAppUrl} from "../App";
import "./RoomList.css";

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
        {roomList.map((roomId, index) => {
          const url = baseAppUrl + "chat/" + roomId + "/" + props.userId;
          return (
            <p className="roomIdItem" key={index}>
              <a>{roomId}</a>
              {/* FIXME THIS DOES NOT WORK ON LOCALHOST due to "unkown protocol". */}
              <button className="button" onClick={() => {
                window.location.href = url;
              }}> Join room
              </button>
              <button className="button" onClick={() => {
                navigator.clipboard.writeText(url);
              }}> copy join code
              </button>
            </p>
          );
        })}
        <button onClick={handleRefresh}>Refresh</button>
      </div>

    </div>
  );
};