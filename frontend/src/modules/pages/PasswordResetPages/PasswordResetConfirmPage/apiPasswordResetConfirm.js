import api from "../../../../api";

export const resetPasswordConfirm = (e, newPassword1, newPassword2, token, navigate) => {
    e.preventDefault();
    console.log("confirmPassword");
    
    if (newPassword1 !== newPassword2) {
        alert("Ошибка. Поле нового пароля и поле подтверждения пароля должны совпадать.");
    } else {
        api
            .post("/api/password-reset/confirm/", {
                password: newPassword1,
                token: token,
            })
            .then((res) => {
                console.log(res.data);
                navigate("/login");
            })
            .catch((err) => {
                console.log(err);
                alert("Ошибка");
            });
    };
};