/* eslint-disable */

import { FC } from 'react'
import { ChatComp } from './ChatComp'
import RoomCreateJoin from './RoomCreateJoin'
import { Game } from "../Games/TicTacToe/Game";

interface GamePageProps {

}

const GamePage: FC<GamePageProps> = ({ }) => {
    return (
        <div id='reg-bg' className='min-h-screen flex'>
            <div className='backdrop-blur-[2px] backdrop-brightness-90 w-full overflow-x-hidden'>
                <div className='max-w-screen-2xl mx-auto grid grid-cols-2 min-h-screen'>
                    {/* <div className='flex items-center justify-center pt-12'> */}
                    <div className='pt-12 flex flex-col gap-4 px-6 py-8'>
                        <RoomCreateJoin />
                        <ChatComp className='' />
                    </div>
                    {/* </div> */}
                    <div className='bg-white shadow-lg shadow-black min-w-[100vw]'>
                        <Game />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default GamePage
