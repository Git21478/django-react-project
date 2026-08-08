import styles from "../../AuthPage.module.css";
import PageTemplate from "../../../PageTemplate/PageTemplate";
import { useInput } from "../../../../hooks/useInput";
import { resetPassword } from "./apiPasswordResetPage";
import { Link } from "react-router-dom";

function PasswordResetPage() {
  document.title = "Сброс пароля | Магазин";
  const email = useInput("");

  return (
    <PageTemplate>
      <div className={styles.auth_page}>
        <form
          className={styles.auth_form}
          onSubmit={(e) => resetPassword(e, email.value)}
        >
          <h1 className={styles.auth_header}>Сброс пароля</h1>

          <div>
            <input
              className={styles.auth_input}
              {...email.input}
              type="text"
              placeholder="Email"
            />
          </div>

          <div>
            <button type="submit" className={styles.auth_submit_button}>
              Отправить письмо
            </button>
          </div>

          <div className={styles.auth_links}>
            <Link to="/registration">Регистрация</Link>
            <Link to="/login">Вход в аккаунт</Link>
          </div>
        </form>
      </div>
    </PageTemplate>
  );
}

export default PasswordResetPage;
