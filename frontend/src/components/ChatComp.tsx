/* eslint-disable */
import { FC, useState } from 'react';
import { Input } from './ui/input';
import { IoSend } from "react-icons/io5";
import { Button } from './ui/button';
import { FaUser } from "react-icons/fa";
import { PiCaretDownBold } from "react-icons/pi";
import { cn } from '../lib/utils';


interface ChatCompProps {

}

const ChatComp: FC<ChatCompProps> = ({ }) => {
    const [closed, setClosed] = useState(false);

    return (
        <div className='max-w-md mx-auto'>
            <div className='bg-slate-900 rounded-t-md flex items-center relative p-2'>
                <p className='text-center font-semibold text-slate-50 flex-1'>Chat</p>
                <Button
                    onClick={() => setClosed(!closed)}
                    className='absolute right-2 hover:bg-slate-800'
                >
                    <PiCaretDownBold className={cn("transition-all", { 'rotate-180': closed })} />
                </Button>
            </div>
            <div className={cn('border border-gray-200 rounded-b-md border-t-0 p-2', { 'hidden': closed })}>
                <div className={``}>
                    <div className='flex items-start flex-col gap-1 mb-5'>
                        <div className='flex justify-center items-center gap-1 text-muted-foreground'>
                            <FaUser className='text-xs' />
                            <p className='text-xs font-semibold'>User 1</p>
                        </div>
                        <p className='border bg-slate-100 p-2 rounded-md w-full text-start text-sm'>some mesage sne by user</p>
                    </div>
                    <div className='flex items-start flex-col gap-1 mb-5'>
                        <div className='flex justify-center items-center gap-1 text-muted-foreground'>
                            <FaUser className='text-xs' />
                            <p className='text-xs font-semibold'>User 1</p>
                        </div>
                        <p className='border bg-slate-100 p-2 rounded-md w-full text-start text-sm'>some mesage sne by user</p>
                    </div>
                    <div className='flex items-start flex-col gap-1 mb-5'>
                        <div className='flex justify-center items-center gap-1 text-muted-foreground'>
                            <FaUser className='text-xs' />
                            <p className='text-xs font-semibold'>User 1</p>
                        </div>
                        <p className='border bg-slate-100 p-2 rounded-md w-full text-start text-sm'>some mesage sne by user</p>
                    </div>
                </div>
                <div className='flex'>
                    <Input className='border-r-0 rounded-r-none' type="text" placeholder="Send message..." />
                    <Button className='rounded-l-none'>
                        <IoSend />
                    </Button>
                </div>
            </div>
        </div>
    )
}

export default ChatComp
