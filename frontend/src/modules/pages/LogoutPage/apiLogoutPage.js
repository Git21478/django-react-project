import api from "../../../api";

export const logout = (setIsAuthenticated) => {
  api
    .post("logout/")
    .then(() => setIsAuthenticated(false))
    .catch((error) => alert(error));
};

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