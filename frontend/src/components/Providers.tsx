/* eslint-disable */

import { UserProvider } from '../hooks/useUser'
import { ChatProvider } from '../hooks/useChat'
import { RoomContextProvider } from '../hooks/useRoom'
import { ReactNode } from 'react'


const Providers = ({ children }: { children: ReactNode }) => {
    return (
        <ChatProvider>
            <RoomContextProvider>
                <UserProvider>
                    {children}
                </UserProvider>
            </RoomContextProvider>
        </ChatProvider>
    )
}

export default Providers
