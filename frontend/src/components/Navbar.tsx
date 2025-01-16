/* eslint-disable */
import { FC } from 'react'
import { FaUser } from 'react-icons/fa'
import { Link } from 'react-router-dom'
import { useUser } from '../hooks/useUser'
import { Button } from './ui/button'

interface NavbarProps {

}

const Navbar: FC<NavbarProps> = ({ }) => {
    const { isAuthenticated, logout } = useUser();

    return (
        <nav className='border-b-4 shadow-lg z-20 border-b-blue-600 fixed top-0 bg-white w-full'>
            <div className="flex justify-between items-center p-4 max-w-screen-xl mx-auto">
                <div className="text-2xl font-bold">Kurnik-2</div>
                <div className="flex items-center justify-center gap-4">
                    <Link to="/chat" className="text-base font-semibold border-b-4 border-t-4 border-white hover:border-b-blue-600 px-2">Play</Link>
                    <Link to="#" className="text-base font-semibold border-b-4 border-t-4 border-white hover:border-b-blue-600 px-2">Todo</Link>
                    <Link to="#" className="text-base font-semibold border-b-4 border-t-4 border-white hover:border-b-blue-600 px-2">Todo</Link>
                </div>
                {isAuthenticated ? (<>
                    <Button onClick={() => logout()} className='hover:bg-blue-500 rounded-full bg-blue-600 text-white font-semibold text-sm px-6'     >
                        <FaUser />
                        <p>logout</p>
                    </Button>
                </>) : (<>
                    <Button className='hover:bg-blue-500 rounded-full bg-blue-600 text-white font-semibold text-sm px-6'    >
                        <FaUser />
                        <Link to="/login">login</Link>
                    </Button>
                </>)}
            </div>
        </nav>
    )
}

export default Navbar
