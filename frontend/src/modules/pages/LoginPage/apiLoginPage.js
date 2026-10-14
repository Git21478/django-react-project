import api from "../../../api";

export const login = (e, email, password, setIsAuthenticated, navigate) => {
  e.preventDefault();
  api
    .post("login/", {
      email: email.value,
      password: password.value,
    })
    .then((_) => {
      setIsAuthenticated(true);
      navigate("/", { replace: true });
    })
    .catch((error) => {
      alert(error);
    });
};
