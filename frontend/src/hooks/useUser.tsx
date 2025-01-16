/* eslint-disable */

import { createContext, ReactNode, useContext, useState } from "react";
import { api } from "../lib/api";

interface UserContextType {
    getToken: () => string | null;
    isAuthenticated: boolean;
    login: (username: string, password: string) => Promise<{ success: boolean; detail: string }>;
    logout: () => void;
    register: (username: string, email: string, password: string) => Promise<{ success: boolean; detail: string }>;
}
const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        const token = getToken();
        if (token) {
            return true;
        }
        return false;
    });

    function setToken(token: string) {
        localStorage.setItem("access_token", token);
        setIsAuthenticated(true);
    }

    async function register(username: string, email: string, password: string) {
        try {
            const response = await api.register(username, email, password);

            return response;
        } catch (error) {
            return {
                success: false,
                detail: "Something went wrong. Please try again.",
            }
        }
    }

    async function login(username: string, password: string) {
        try {
            const response = await api.login(username, password);

            if (response.success) {
                setToken(response.data?.accessToken);
                setIsAuthenticated(true);
                return {
                    success: true,
                    detail: "Login successful",
                }
            } else {
                return {
                    success: false,
                    detail: "Something went wrong",
                }
            }
        } catch (error) {
            return {
                success: false,
                detail: "Something went wrong. Please try again.",
            }
        }
    }

    function logout() {
        localStorage.removeItem("access_token");
        setIsAuthenticated(false);
    }

    function getToken() {
        return localStorage.getItem("access_token");
    }

    return (
        <UserContext.Provider value={{ isAuthenticated, getToken, login, logout, register }}>
            {children}
        </UserContext.Provider>
    );
}

export const useUser = (): UserContextType => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error("useChat must be used within a ChatProvider");
    }
    return context;
};
