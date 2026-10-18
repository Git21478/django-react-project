import api from "../../../api";

export const logout = (setUser, setIsAuthenticated) => {
  api
    .post("logout/")
    .then(() => {
        setUser(null);
        setIsAuthenticated(false);
    })
    .catch((error) => console.log(error));
};