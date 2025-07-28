import api from "../../../api";

export const register = (e, email, username, password, confirmPassword, navigate) => {
    e.preventDefault();
    if (password.value === confirmPassword.value) {
        api
            .post("api/user/registration/", {
                email: email.value,
                username: username.value,
                password: password.value,
            })
            .then(() => {
                navigate("/login");
            })
            .catch((error) => {
                alert(error);
            });
    }
    else alert("Введёные пароли не совпадают.");
};