/* eslint-disable */
import { FC, useState } from 'react';
import { FaUser } from "react-icons/fa";
import { GrKeyboard } from "react-icons/gr";
import { IoSend } from "react-icons/io5";
import { PiCaretDownBold } from "react-icons/pi";
import { useChat } from '../hooks/useChat';
import { cn } from '../lib/utils';
import { Button } from './ui/button';
import { Input } from './ui/input';


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
    const [typedMessage, setTypedMessage] = useState<string>('')
    const { messageList, sendMessageF } = useChat()

    return (
        <div className={cn('flex flex-col mx-auto w-full shadow-md shadow-zinc-800', className, { 'h-full': !closed })}>
            <div className=' bg-slate-900 rounded-t-md flex items-center relative p-2'>
                <p className='text-center font-semibold text-slate-50 flex-1'>Chat</p>
                <Button
                    onClick={() => setClosed(!closed)}
                    className='absolute right-2 hover:bg-slate-800'
                >
                    <PiCaretDownBold className={cn("transition-all", { 'rotate-180': closed })} />
                </Button>
            </div>
            <div className={cn('h-full flex flex-col border border-gray-200 bg-white rounded-b-md border-t-0 p-2 max-h-[80vh]', { 'hidden': closed })}>
                <div className={cn(`h-full overflow-y-scroll`, messageList.length === 0 ? `flex ` : '')}>
                    {messageList.map((message, index) => {
                        return (
                            <MessageComp key={index} message={message.data} username={'user FIX'} />
                        )
                    })}
                    {messageList.length === 0 && (
                        <div className=' flex justify-center items-center flex-col my-16 opacity-15 max-w-[75%] mx-auto'>
                            <GrKeyboard className='text-7xl' />
                            <p className='text-xl'>Join chat, and messages you write will appear here.</p>
                        </div>
                    )}
                </div>
                <div className='flex '>
                    <Input value={typedMessage} onChange={(e) => setTypedMessage(e.currentTarget.value)} className='border-r-0 rounded-r-none' type="text" placeholder="Send message..." />
                    <Button className='rounded-l-none' onClick={() => {
                        sendMessageF(typedMessage)
                        setTypedMessage('')
                    }}>
                        <IoSend />
                    </Button>
                </div>
            </div>
        </div>
    )
}

export { ChatComp, MessageComp };
