import api from "../../../api";

export const login = (e, email, password, setIsAuthenticated, navigate) => {
  e.preventDefault();
  api
    .post("login/", { email, password })
    .then((_) => {
      setIsAuthenticated(true);
      navigate("/", { replace: true });
    })
    .catch((error) => {
      console.error(error);
    });
};
