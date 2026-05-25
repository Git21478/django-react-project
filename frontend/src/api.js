import axios from "axios";
import { ACCESS_TOKEN, backendBaseURL } from "./constants";

const generateUUID = () => {
    if (typeof crypto !== "undefined" && crypto.generateUUID) {
        return crypto.generateUUID;
    };

    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(char) {
        const r = Math.random() * 16 | 0;
        const v = char === "x" ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
};

const getOrCreateSessionKey = () => {
    const SESSION_KEY = "session_key";
    let sessionKey = localStorage.getItem(SESSION_KEY);

    if (!sessionKey) {
        sessionKey = generateUUID();
        localStorage.setItem(SESSION_KEY, sessionKey)
    };

    return sessionKey;
};

const api = axios.create({
    baseURL: backendBaseURL,
    withCredentials: true,
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        else {
            const sessionKey = getOrCreateSessionKey();
            config.headers["X-Session-Key"] = sessionKey;
        };
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => {
        if (response.config.url?.includes("/token/") && response.data?.cart_merged) {
            localStorage.removeItem("session_key");
        }

        return response;
    }
);

export default api;