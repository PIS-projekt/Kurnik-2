/* eslint-disable */

import { FC } from 'react';
import { Game } from "../Games/TicTacToe/Game";
import { ChatComp } from './ChatComp';
import RoomCreateJoin from './RoomCreateJoin';
import PublicRoomsList from "./PublicRoomsList";

interface GamePageProps {

}

const GamePage: FC<GamePageProps> = ({ }) => {
    return (
        <div id='reg-bg' className='min-h-screen flex'>
            <div className='backdrop-blur-[2px] backdrop-brightness-90 w-full overflow-x-hidden'>
                <div className='max-w-screen-2xl mx-px grid grid-cols-3 min-h-screen'>
                    <div className="mt-20 flex flex-col gap-4 px-10 py-8">
                        <PublicRoomsList />
                    </div>
                    <div className='pt-12 flex flex-col gap-4 px-6 py-8'>

                        <RoomCreateJoin />
                        <ChatComp className='' />
                    </div>
                    <div className='bg-white shadow-lg ml-20 shadow-black min-w-[40vw] flex items-center justify-center'>
                        <div>
                            <Game />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default GamePage
