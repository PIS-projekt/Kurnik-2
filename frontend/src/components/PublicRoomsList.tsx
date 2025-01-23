/* eslint-disable */
import { FC, useEffect, useState } from "react";
import axios from "axios";

const PublicRoomsList: FC = () => {
    const [rooms, setRooms] = useState<string[]>([]);

    const apiBaseUrl = "http://0.0.0.0:8000";

    // Fetch the list of public rooms on component mount
    useEffect(() => {
        const fetchPublicRooms = async () => {
            try {
                // Update with the correct API base if needed
                const response = await axios.get(`${apiBaseUrl}/get-public-rooms`);
                setRooms(response.data.rooms || []);
            } catch (error) {
                console.error("Failed to fetch public rooms:", error);
            }
        };
        fetchPublicRooms();
    }, []);

    // Function to copy room ID to clipboard using a <textarea>
    const copyToClipboard = (roomId: string) => {
        const textarea = document.createElement("textarea");
        textarea.value = roomId;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy"); // Some environments may require 'document.execCommand("copy")'
        document.body.removeChild(textarea);
        console.log(`Copied Room ID: ${roomId}`);
    };

    return (
        <div className="bg-white p-4 rounded shadow">
            <h2 className="font-bold text-lg mb-2">Public Rooms</h2>
            <ul className="space-y-2">
                {rooms.map((roomId) => (
                    <li
                        key={roomId}
                        className="cursor-pointer hover:text-blue-600 transition-colors flex items-center"
                        onClick={() => copyToClipboard(roomId)}
                    >
                        {roomId} <span className="ml-2">📋</span>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PublicRoomsList;
