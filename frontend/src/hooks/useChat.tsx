/* eslint-disable */

import { useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { useRoom } from "./useRoom";

export function useChat() {
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

}
