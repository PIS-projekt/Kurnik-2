/* eslint-disable */
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Input } from "./ui/input";
import { FaUser } from "react-icons/fa";
import { Separator } from "./ui/separator";
import { MdEmail } from "react-icons/md";
import { RiLockPasswordFill } from "react-icons/ri";
import { api } from "../lib/api";
import { useUser } from "../hooks/useUser";

export function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const navigate = useNavigate();
    const { register } = useUser()

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        const res = await register(username, email, password)
        if (res.success) {
            setSuccess("Registration successful! Please log in.");
            setTimeout(() => navigate("/login"), 1000);
        } else {
            setError("Registration failed");
        }
    };

    return (
        <div id="reg-bg" className="bg-gradient-to-t from-blue-600 to-blue-900 min-h-screen flex items-center justify-center">
            <div className="max-w-lg bg-white w-full rounded-lg shadow-lg p-6 flex flex-col justify-center">
                <h2 className="mx-auto bg-gradient-to-r from-blue-600 to-blue-900 font-extrabold text-clip inline-block bg-clip-text text-4xl text-transparent">Register</h2>
                <form onSubmit={handleRegister} className="mt-12">
                    <div className="flex items-center justify-center flex-col gap-4">
                        <div className="bg-slate-100 rounded-full border flex items-center justify-start py-2 px-4 gap-2 font-semibold">
                            <FaUser className="text-slate-400" />
                            <input
                                className="bg-transparent focus:outline-none"
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                required
                                placeholder="Username"
                            />
                        </div>
                        <div className="bg-slate-100 rounded-full border flex items-center justify-start py-2 px-4 gap-2 font-semibold">
                            <MdEmail className="text-slate-400" />
                            <input
                                className="bg-transparent focus:outline-none"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                placeholder="Email"
                            />
                        </div>
                        <div className="bg-slate-100 rounded-full border flex items-center justify-start py-2 px-4 gap-2 font-semibold">
                            <RiLockPasswordFill className="text-slate-400" />
                            <input
                                className="bg-transparent focus:outline-none"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                placeholder="Password"
                            />
                        </div>
                    </div>
                    <div className="w-fit mt-12 grid grid-cols-2 gap-4 mx-auto">
                        <button
                            className="font-semibold hover:bg-slate-100 p-2 px-4 rounded-full text-muted-foreground "
                            onClick={() => navigate("/login")}>
                            back to login
                        </button>
                        <button
                            type="submit"
                            className="before:w-full before:h-full before:bg-gradient-to-b before:from-transparent before:to-blue-800 before:hover:opacity-0 before:transition-all before:absolute relative before:left-0 before:top-0 before:-z-10 z-10 transition-all bg-blue-600 rounded-full before:rounded-full p-2 px-4 font-semibold text-white"
                        >register</button>
                    </div>
                </form>
                {error && <p style={{ color: "red" }}>{error}</p>}
                {success && <p style={{ color: "green" }}>{success}</p>}
            </div>
        </div>
    );
}
