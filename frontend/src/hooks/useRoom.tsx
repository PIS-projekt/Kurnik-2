import {createContext, ReactNode, useContext, useState} from "react";

interface RoomContextData {
  roomCode: string;
  setRoomCode: (roomCode: string) => void;
}


const RoomContext = createContext<RoomContextData | null>(null);

export const RoomContextProvider = ({children}: { children: ReactNode }) => {
  const [roomCode, setRoomCode] = useState<string>("");
  return <RoomContext.Provider value={{roomCode, setRoomCode}}>
    {children}
  </RoomContext.Provider>;
};


export const useRoom = (): RoomContextData => useContext(RoomContext)!;