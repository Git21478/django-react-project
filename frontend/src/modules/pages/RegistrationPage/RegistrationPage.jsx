import styles from "../AuthPage.module.css";
import { useNavigate } from "react-router-dom";
import { useInput } from "../../../hooks/useInput";
import { register } from "./apiRegistrationPage";
import PageTemplate from "../../PageTemplate/PageTemplate";

function RegistrationPage() {
    document.title = "Регистрация | Магазин";
    const navigate = useNavigate();
    const email = useInput("");
    const username = useInput("");
    const password = useInput("");
    const confirmPassword = useInput("");

    return (
        <PageTemplate>
            <div className={styles.auth_page}>
                <form onSubmit={(e) => register(e, email, username, password, confirmPassword, navigate)} className={styles.auth_form}>
                    <h2 className={styles.auth_header}>Регистрация</h2>

                    <div>
                        <input
                            {...email.input}
                            type="text"
                            placeholder="Email"
                            className={styles.auth_input}
                        />
                    </div>

                    <div>
                        <input
                            {...username.input}
                            type="text"
                            placeholder="Имя пользователя"
                            className={styles.auth_input}
                            required
                        />
                    </div>

                    <div>
                        <input
                            {...password.input}
                            type="password"
                            placeholder="Пароль"
                            autoComplete="off"
                            className={styles.auth_input}
                            required
                        />
                    </div>

                    <div>
                        <input
                            {...confirmPassword.input}
                            type="password"
                            placeholder="Подтверждение пароля"
                            autoComplete="off"
                            className={styles.auth_input}
                            required
                        />
                    </div>

                    <div className={styles.auth_buttons}>
                        <div>
                            <button type="submit" className={styles.auth_submit_button}>
                                Зарегистрироваться
                            </button>
                        </div>

                        <div className={styles.auth_links}>
                            <span></span>
                            <a href="/login">Вход в аккаунт</a>
                        </div>
                    </div>
                </form>
            </div>
        </PageTemplate>
    );
};

export default RegistrationPage;