/* eslint-disable */

import { createContext, ReactNode, useContext, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

interface ChatContextType {
    messageList: Array<{ data: string }>;
    joinRoomChat: (roomCode: string, token: string) => void;
    sendMessageF: (message: string) => void;
}
const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [socketUrl, setSocketUrl] = useState<string | null>(null);
    const [messageList, setMessageList] = useState<Array<{ data: string }>>([]);

    const apiBaseUrl = "http://0.0.0.0:8000";

    const handleOpen = () => {
        console.log("WebSocket connection opened.");
    };

    const handleClose = () => {
        console.log("WebSocket connection closed.");
        setMessageList([]);
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

    async function joinRoomChat(roomCode: string, token: string) {
        setSocketUrl(`${apiBaseUrl}/ws/connect/${roomCode}?token=${token}`);
    }

    async function sendMessageF(message: string) {
        if (message && readyState === ReadyState.OPEN) {
            sendMessage(message);
        }
    }

    return (
        <ChatContext.Provider value={{ messageList, joinRoomChat, sendMessageF }}>
            {children}
        </ChatContext.Provider>
    );
}

export const useChat = (): ChatContextType => {
    const context = useContext(ChatContext);
    if (!context) {
        throw new Error("useChat must be used within a ChatProvider");
    }
    return context;
};
