import api from "../../../../api";

export const changePassword = (oldPassword, newPassword1, newPassword2, navigate) => {
    if (oldPassword === newPassword1) {
        alert("Ошибка. Поле старого пароля и поле нового пароля не должны совпадать.");
    } else if (newPassword1 !== newPassword2) {
        alert("Ошибка. Поле нового пароля и поле подтверждения пароля должны совпадать.");
    } else {
        api
            .put("/api/password-change/", {
                old_password: oldPassword,
                new_password: newPassword1,
            })
            .then((res) => {
                if (res.status === 200) {
                    localStorage.clear();
                    navigate("/login");
                    console.log("Пароль успешно изменён.");
                }
                else alert("Ошибка при попытке изменения пароля.");
            })
            .catch((error) => alert(error));
    };
};