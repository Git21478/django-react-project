import api from "../../api";
import { jwtDecode } from "jwt-decode";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../../constants";

const refreshToken = async (setIsAuthenticated) => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN);   
    api
        .post("/api/token/refresh/", {
            refresh: refreshToken,
        })
        .then((res) => {
            if (res.status == 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                setIsAuthenticated(true);
            } else {
                setIsAuthenticated(false);
                console.log("Authorization failed.");
            };
        })
        .catch((error) => {
        if (error.response?.status === 401) {
            console.log(error);
            localStorage.removeItem(ACCESS_TOKEN);
            localStorage.removeItem(REFRESH_TOKEN);
        }
            setIsAuthenticated(false);
        });
};

export const auth = async (setIsAuthenticated) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (!token) {
        setIsAuthenticated(false);
        return;
    };
    const decoded = jwtDecode(token);
    const tokenExpiration = decoded.exp;
    const now = Date.now() / 1000;

    if (tokenExpiration < now) {
        await refreshToken(setIsAuthenticated);
    } else {
        setIsAuthenticated(true);
    };
};