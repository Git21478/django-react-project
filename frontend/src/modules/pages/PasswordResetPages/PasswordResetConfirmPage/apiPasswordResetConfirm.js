import api from "../../../../api";

export const resetPasswordConfirm = (
  e,
  newPassword1,
  newPassword2,
  token,
  navigate,
) => {
  e.preventDefault();

  if (newPassword1 !== newPassword2) {
    alert(
      "Ошибка. Поле нового пароля и поле подтверждения пароля должны совпадать.",
    );
  } else {
    api
      .post("/api/password-reset/confirm/", {
        password: newPassword1,
        token: token,
      })
      .then((_) => {
        navigate("/login");
      })
      .catch((error) => {
        console.error(error);
        alert("Ошибка");
      });
  }
};
