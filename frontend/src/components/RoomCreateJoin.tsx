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
import { useUser } from '../hooks/useUser';
import { useRoom } from '../hooks/useRoom';

interface RoomCreateJoinProps {

}

const RoomCreateJoin: FC<RoomCreateJoinProps> = ({ }) => {
    const { joinRoomChat } = useChat()
    const { getToken } = useUser()
    const { roomCode, setRoomCode } = useRoom();

    const [joinRoomId, setJoinRoomId] = useState<string>('');
    const [isPrivate, setIsPrivate] = useState<boolean>(false);

    return (
        <div className='border rounded-sm p-4 mx-auto mt-12 bg-white w-full shadow-md shadow-zinc-800'>
            <div className='flex items-center justify-center gap-2'>
                <p className='text-3xl font-semibold'>Room:</p>
                {roomCode ?
                    (
                        <div className='border rounded-md flex items-center py-1'>
                            <p className='text-xl font-semibold border-r px-3'>{roomCode}</p>
                            <TooltipProvider>
                                <Tooltip delayDuration={0}>
                                    <TooltipTrigger asChild>
                                        <Button variant='ghost' className='p-0 aspect-square' onClick={() => {
                                            const textarea = document.createElement('textarea');
                                            textarea.value = roomCode;
                                            document.body.appendChild(textarea);
                                            textarea.select();
                                            document.execCommand('copy');
                                            toast.success('Room ID copied to clipboard 📋');
                                            document.body.removeChild(textarea);
                                        }}>
                                            <IoCopy />
                                        </Button>
                                    </TooltipTrigger>
                                    <TooltipContent>
                                        <p>Copy room ID</p>
                                    </TooltipContent>
                                </Tooltip>
                            </TooltipProvider>
                            {/* <TooltipProvider>
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
                            </TooltipProvider> */}
                        </div>
                    )
                    :
                    (
                        /* Create new room button with isPrivate checkbox */
                        <div className='flex flex-col items-center gap-2'>
                            <Button
                                className='mt-3'
                                onClick={async () => {
                                    try {
                                        const token = getToken();
                                        if (!token) {
                                            toast.error('No token found.');
                                            return;
                                        }
                                        // Create the room (private or public) based on isPrivate
                                        const roomId = await api.createRoom(token, isPrivate);
                                        setRoomCode(roomId);
                                        // Immediately join the newly created room
                                        joinRoomChat(roomId, token);
                                    } catch (error) {
                                        console.error('Error creating room:', error);
                                        toast.error('Failed to create room.');
                                    }
                                }}
                            >
                                <p>Create</p>
                                <FaPlus />
                            </Button>
                            <div className='flex items-center gap-2'>
                                <label htmlFor='privateRoom' className='text-sm font-medium'>
                                    Private
                                </label>
                                <input
                                    id='privateRoom'
                                    type='checkbox'
                                    checked={isPrivate}
                                    onChange={(e) => setIsPrivate(e.target.checked)}
                                />
                            </div>
                        </div>
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
                    setRoomCode(joinRoomId)
                    await api.joinRoom(joinRoomId, getToken()!)
                    joinRoomChat(joinRoomId, getToken()!)
                }}>
                    <p>join</p>
                    <FaArrowRightToBracket />
                </Button>
            </div>
        </div >
    )
}

export default RoomCreateJoin
