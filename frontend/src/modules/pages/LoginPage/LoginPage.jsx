import styles from "../AuthPage.module.css";
import { useInput } from "../../../hooks/useInput.js";
import { login } from "./apiLoginPage.js";
import { useNavigate } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { useValidation } from "../../../hooks/useValidation.js";
import PageTemplate from "../../PageTemplate/PageTemplate.jsx";
import { AppContext } from "../../AppProvider/AppProvider.jsx";

function LoginPage() {
    document.title = "Вход в аккаунт | Магазин";
    const appData = useContext(AppContext);
    const navigate = useNavigate();
    const email = useInput("");
    const password = useInput("");
    const [isFormValid, setIsFormValid] = useState(true);

    // useValidation(email.value, [
    //     {name: "isEmpty", value: false, errorMessage: "Поле не должно быть пустым"},
    //     {name: "minLength", value: 3, errorMessage: "Длина email не должна быть меньше 3"},
    //     {name: "maxLength", value: 8, errorMessage: "Длина email не должна быть больше 8"},
    // ]);

    return (
        <PageTemplate>
            <div className={styles.auth_page}>
                <form className={styles.auth_form} onSubmit={(e) => {
                    login(e, email, password, appData.setIsAuthenticated, navigate);
                }}>
                    <h2 className={styles.auth_header}>Вход в аккаунт</h2>

                    {/* {!emailValidation.isValid && <div style={{ color: "red" }}>Некорректная почта</div>} */}
                    {!isFormValid && <div style={{ color: "red" }}>Некорректная почта</div>}
                    <div>
                        <input
                            type="text"
                            {...email.input}
                            placeholder="Email"
                            className={styles.auth_input}
                        />
                    </div>

                    {!isFormValid && <div style={{ color: "red" }}>Некорректный пароль</div>}
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
                            <a href="/password-reset">Забыли пароль?</a>
                            <a href="/registration">Регистрация</a>
                        </div>
                    </div>
                </form>
            </div>
        </PageTemplate>
    );
};

export default LoginPage;