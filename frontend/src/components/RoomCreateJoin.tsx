/* eslint-disable */

import { FC, useState } from 'react';
import { FaLink, FaPlus } from "react-icons/fa";
import { FaArrowRightToBracket } from "react-icons/fa6";
import { IoCopy } from "react-icons/io5";
import { useChat } from '../hooks/useChat';
import { api } from '../lib/api';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip';
import toast from 'react-hot-toast';

interface RoomCreateJoinProps {

}

const RoomCreateJoin: FC<RoomCreateJoinProps> = ({ }) => {
    const { joinRoomChat } = useChat()

    const [roomId, setRoomId] = useState<string>('')
    const [joinRoomId, setJoinRoomId] = useState<string>('')
    const USER_ID = 1

    return (
        <div className='border shadow-sm rounded-sm p-4 max-w-[25vw] mx-auto mt-12'>
            <div className='flex items-center justify-center gap-2'>
                <p className='text-3xl font-semibold'>Room:</p>
                {roomId ?
                    (
                        <div className='border rounded-md flex items-center py-1'>
                            <p className='text-xl font-semibold border-r px-3'>{roomId}</p>
                            <TooltipProvider>
                                <Tooltip delayDuration={0}>
                                    <TooltipTrigger asChild>
                                        <Button variant='ghost' className='p-0 aspect-square' onClick={() => {
                                            navigator.clipboard.writeText(roomId)
                                            toast.success('Room ID copied to clipboard')
                                        }}>
                                            <IoCopy />
                                        </Button>
                                    </TooltipTrigger>
                                    <TooltipContent>
                                        <p>Copy room ID</p>
                                    </TooltipContent>
                                </Tooltip>
                            </TooltipProvider>
                            <TooltipProvider>
                                <Tooltip delayDuration={0}>
                                    <TooltipTrigger asChild>
                                        <Button variant='ghost' className='p-0 aspect-square' onClick={() => {
                                            toast.success('Room URL copied to clipboard')
                                        }}>
                                            <FaLink />
                                        </Button>
                                    </TooltipTrigger>
                                    <TooltipContent>
                                        <p>Copy URL</p>
                                    </TooltipContent>
                                </Tooltip>
                            </TooltipProvider>
                        </div>
                    )
                    :
                    (
                        <Button className='' onClick={async () => {
                            const roomId = await api.createRoom(USER_ID)
                            setRoomId(roomId)
                            joinRoomChat(roomId, USER_ID)
                        }}>
                            <p>create</p>
                            <FaPlus />
                        </Button>
                    )}
            </div>
            <div className='flex justify-center items-center gap-2 my-6'>
                <div className='bg-slate-200 h-[1px] w-full'></div>
                <p className='font-bold opacity-35'>or</p>
                <div className='bg-slate-200 h-[1px] w-full'></div>
            </div>
            <div className='flex items-center justify-center'>
                <Input value={joinRoomId} placeholder='Room ID' onChange={(e) => setJoinRoomId(e.currentTarget.value)} className='max-w-36 rounded-r-none border-r-0' />
                <Button className='rounded-l-none' onClick={async () => {
                    setRoomId(joinRoomId)
                    await api.joinRoom(joinRoomId, USER_ID)
                    joinRoomChat(joinRoomId, USER_ID)
                }}>
                    <p>join</p>
                    <FaArrowRightToBracket />
                </Button>
            </div>
        </div >
    )
}

export default RoomCreateJoin
