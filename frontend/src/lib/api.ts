/* eslint-disable */
import axios from "axios";

export const api = {
    async createRoom(token: string): Promise<string> {
        const response = await axios.get(`http://0.0.0.0:8000/create-new-room`, {
            params: { private: false },
            headers: { Authorization: `Bearer ${token}` },
        });
        const newRoomCode = response.data.room_code;
        return newRoomCode;
    },

    async joinRoom(roomCode: string, token: string): Promise<boolean> {
        const response = await axios.get(`http://0.0.0.0:8000/join-room`, {
            params: { room_code: roomCode },
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.data.room_exists
    },

    async register(username: string, email: string, password: string) {
        const response = await fetch("http://0.0.0.0:8000/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
            }),
        });

        if (response.ok) {
            return {
                success: true,
                detail: "User registered successfully.",
            }
        }

        return {
            success: false,
            detail: "User registration failed.",
        }
    },

    async login(username: string, password: string) {

        const response = await fetch("http://0.0.0.0:8000/auth/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                username: username,
                password: password,
            }),
        });



        if (response.ok) {
            const data = await response.json();
            return {
                success: true,
                detail: "Login successful",
                data: {
                    accessToken: data.access_token
                }
            }
        }

        return {
            success: false,
            detail: "something went wrong",
        }
    }
}
