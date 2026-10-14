import api from "../../api";

export const getUser = (setUser, setIsAuthenticated) => {
  api
    .get("user/me/")
    .then((res) => {
      setUser(res.data);
      setIsAuthenticated(true);
    })
    .catch((error) => {
      setUser(null);
      setIsAuthenticated(false);
      console.error(error);
    });
};
