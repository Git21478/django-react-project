import axios from "axios";
import { ACCESS_TOKEN, backendBaseURL } from "./constants";

const api = axios.create({
    baseURL: backendBaseURL
});

api.interceptors.request.use(
    (config) => {
        const publicPaths = ["/categories", "/products"];
        const isPublic = publicPaths.some(path => config.url.includes(path));

        if (!isPublic) {
            const token = localStorage.getItem(ACCESS_TOKEN);
            if (token) {
                config.headers.Authorization = `Bearer ${token}`
            };
        };
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;