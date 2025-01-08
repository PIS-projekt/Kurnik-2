import {FormEvent, useEffect, useState} from "react";
import axios from "axios";
import {apiBaseUrl} from "../App";

export const RoomList = () => {

  const [roomList, setRoomList] = useState<Array<number>>([]);

  const handleRefresh = async  () => {
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
      <div id="RoomList">
        <h2>Public rooms: </h2>
        {roomList.map((roomId, index) => (
          <p className="roomIdItem" key={index}>
            {roomId}
          </p>
        ))}
        <button onClick={handleRefresh}>Refresh</button>
      </div>

    </div>
  );
};