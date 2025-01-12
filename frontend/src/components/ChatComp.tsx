/* eslint-disable */
import { FC, useEffect, useState } from 'react';
import { Input } from './ui/input';
import { IoSend } from "react-icons/io5";
import { Button } from './ui/button';
import { FaUser } from "react-icons/fa";
import { PiCaretDownBold } from "react-icons/pi";
import { cn } from '../lib/utils';
import axios from 'axios';
import { useChat } from '../hooks/useChat';
import { api } from '../lib/api';
import { GrKeyboard } from "react-icons/gr";


interface MessageCompProps {
    username: string;
    message: string;
}
const MessageComp: FC<MessageCompProps> = ({ message, username }) => {
    return (
        <div className='flex items-start flex-col gap-1 mb-5'>
            <div className='flex justify-center items-center gap-1 text-muted-foreground'>
                <FaUser className='text-xs' />
                <p className='text-xs font-semibold'>{username}</p>
            </div>
            <p className='border bg-slate-100 p-2 rounded-md w-full text-start text-sm'>{message}</p>
        </div>
    )
}

interface ChatCompProps {
    className?: string;
}
const ChatComp: FC<ChatCompProps> = ({ className }) => {
    const [closed, setClosed] = useState(false);
    // const { messageList } = useChat()
    const messageList = [
        {
            data: "xd"
        },
        {
            data: "xd"
        },
    ]

    return (
        <div className={cn('flex flex-col max-w-md mx-auto w-full', className)}>
            {/* <Button onClick={() => {
                api.createRoom(1).then((roomCode) => {
                    console.log(roomCode)
                    // @ts-ignore
                    window.roomCode = roomCode
                })
            }}>
                create
            </Button>
            <Button onClick={() => {
                // @ts-ignore
                api.joinRoom(window.roomCode, 2).then((roomCode) => {
                    console.log(roomCode)
                    // eslint-disable-next-line no-undef
                    // @ts-ignore
                    console.log(window.roomCode)
                })
            }}>
                join
            </Button>
            <Button onClick={() => {
                // @ts-ignore
                joinRoomChat(window.roomCode, 1)
            }
            }>
                join chat
            </Button>
            <Button onClick={() => {
                sendMessageF('some message')
            }}>
                msg
            </Button> */}
            <div className=' bg-slate-900 rounded-t-md flex items-center relative p-2'>
                <p className='text-center font-semibold text-slate-50 flex-1'>Chat</p>
                <Button
                    onClick={() => setClosed(!closed)}
                    className='absolute right-2 hover:bg-slate-800'
                >
                    <PiCaretDownBold className={cn("transition-all", { 'rotate-180': closed })} />
                </Button>
            </div>
            <div className={cn('flex flex-col border border-gray-200 rounded-b-md border-t-0 p-2 max-h-[80vh]', { 'hidden': closed })}>
                <div className={`overflow-y-scroll`}>
                    {messageList.map((message, index) => {
                        return (
                            <MessageComp key={index} message={message.data} username={'user FIX'} />
                        )
                    })}
                    {messageList.length === 0 && (
                        <div className='flex justify-center items-center flex-col my-16 opacity-15 max-w-[75%] mx-auto'>
                            <GrKeyboard className='text-7xl' />
                            <p className='text-xl'>Join chat, and messages you write will appear here.</p>
                        </div>
                    )}
                    {/* <MessageComp message='some message' username='user 1' />
                    <MessageComp message='some message' username='user 1' />
                    <MessageComp message='some message' username='user 1' /> */}
                </div>
                <div className='flex '>
                    <Input className='border-r-0 rounded-r-none' type="text" placeholder="Send message..." />
                    <Button className='rounded-l-none'>
                        <IoSend />
                    </Button>
                </div>
            </div>
        </div>
    )
}

export { ChatComp, MessageComp }
