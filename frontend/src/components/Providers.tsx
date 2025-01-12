/* eslint-disable */

import { ChatProvider } from '../hooks/useChat'
import { RoomContextProvider } from '../hooks/useRoom'
import { ReactNode } from 'react'


const Providers = ({ children }: { children: ReactNode }) => {
    return (
        <ChatProvider>
            <RoomContextProvider>
                {children}
            </RoomContextProvider>
        </ChatProvider>
    )
}

export default Providers
