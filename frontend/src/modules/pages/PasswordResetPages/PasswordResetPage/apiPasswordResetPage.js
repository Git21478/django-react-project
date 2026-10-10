import api from "../../../../api";

export const resetPassword = (e, email) => {
  e.preventDefault();
  api
    .post("/api/password-reset/", {
      email: email,
    })
    .then((res) => {
      alert(
        "Сообщение со ссылкой для востановления пароля отправлено на вашу почту.",
      );
    })
    .catch((error) => {
      console.error(error);
      alert("Ошибка");
    });
};
