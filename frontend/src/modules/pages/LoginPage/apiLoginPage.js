import api from "../../../api";

export const login = (e, email, password, setIsAuthenticated, navigate) => {
  e.preventDefault();
  api
    .post("/api/login/", {
      email: email.value,
      password: password.value,
    })
    .then((res) => {
      setIsAuthenticated(true);
      navigate("/", { replace: true });
    })
    .catch((error) => {
      alert(error);
    });
};
