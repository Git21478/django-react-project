import api from "../../../api";

export const logout = (setIsAuthenticated) => {
  api
    .post("/api/logout/")
    .then(() => setIsAuthenticated(false))
    .catch((error) => alert(error));
};