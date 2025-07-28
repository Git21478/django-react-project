import api from "../../../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../../constants";

export const login = (e, email, password, setIsAuthenticated, navigate) => {
    e.preventDefault();
    api
        .post("api/token/", {
            email: email.value,
            password: password.value,
        })
        .then((res) => {
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
            setIsAuthenticated(true);
            navigate("/");
        })
        .catch((error) => {
            alert(error);
        });
};