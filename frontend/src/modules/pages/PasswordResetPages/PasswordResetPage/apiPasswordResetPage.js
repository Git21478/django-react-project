import api from "../../../../api";

export const resetPassword = (e, email) => {
    e.preventDefault();
    console.log("resetPassword");
    api
        .post("/api/password-reset/", {
            email: email,
        })
        .then((res) => {
            console.log(res.data);
            alert("Сообщение со ссылкой для востановления пароля отправлено на вашу почту.");
        })
        .catch((err) => {
            console.log(err);
            alert("Ошибка");
        });
};