/* eslint-disable */
import axios from "axios";

export const api = {
    async createRoom(userId: number): Promise<string> {
        const response = await axios.get(`http://0.0.0.0:8000/create-new-room`, {
            // eslint-disable-next-line camelcase
            params: { user_id: userId, private: false }, // TODO: get setting from user
        });
        const newRoomCode = response.data.room_code;
        return newRoomCode;
    },

    async joinRoom(roomCode: string, userId: number): Promise<boolean> {
        const response = await axios.get(`http://0.0.0.0:8000/join-room`, {
            // eslint-disable-next-line camelcase
            params: { room_code: roomCode, user_id: userId },
        });
        return response.data.room_exists
    }
}
