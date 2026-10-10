import api from "../../api";

export const getUser = async (setUser, setIsAuthenticated) => {
  api
    .get("/api/user/")
    .then((res) => {
      setUser({...res.data[0]});
      setIsAuthenticated(true);
    })
    .catch((error) => {
      setIsAuthenticated(false);
      alert(error);
    });
};
