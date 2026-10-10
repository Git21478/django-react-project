import styles from "../AuthPage.module.css";
import { useInput } from "../../../hooks/useInput.js";
import { login } from "./apiLoginPage.js";
import { Link, useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import PageTemplate from "../../PageTemplate/PageTemplate.jsx";
import { AppContext } from "../../AppProvider/AppProvider.jsx";

function LoginPage() {
  document.title = "Вход в аккаунт | Магазин";
  const { setIsAuthenticated } = useContext(AppContext);
  const navigate = useNavigate();
  const email = useInput("");
  const password = useInput("");
  const [isFormValid, setIsFormValid] = useState(true);

  return (
    <PageTemplate>
      <div className={styles.auth_page}>
        <form
          className={styles.auth_form}
          onSubmit={(e) => {
            login(e, email, password, setIsAuthenticated, navigate);
          }}
        >
          <h2 className={styles.auth_header}>Вход в аккаунт</h2>

          {!isFormValid && (
            <div style={{ color: "red" }}>Некорректная почта</div>
          )}
          <div>
            <input
              type="text"
              {...email.input}
              placeholder="Email"
              className={styles.auth_input}
            />
          </div>

          {!isFormValid && (
            <div style={{ color: "red" }}>Некорректный пароль</div>
          )}
          <div>
            <input
              type="password"
              {...password.input}
              placeholder="Пароль"
              autoComplete="off"
              className={styles.auth_input}
            />
          </div>

          <div className={styles.auth_buttons}>
            <div>
              <button type="submit" className={styles.auth_submit_button}>
                Войти
              </button>
            </div>

            <div className={styles.auth_links}>
              <Link to="/password-reset">Забыли пароль?</Link>
              <Link to="/registration">Регистрация</Link>
            </div>
          </div>
        </form>
      </div>
    </PageTemplate>
  );
}

export default LoginPage;
