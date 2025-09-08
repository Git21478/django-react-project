import styles from "../../AuthPage.module.css";
import PageTemplate from "../../../PageTemplate/PageTemplate";
import { useInput } from "../../../../hooks/useInput";
import { resetPasswordConfirm } from "./apiPasswordResetConfirm";
import { useLocation, useNavigate } from "react-router-dom";

function PasswordResetConfirmPage() {
    document.title = "Новый пароль | Магазин";
    const navigate = useNavigate();
    
    const newPassword1 = useInput("");
    const newPassword2 = useInput("");

    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const token = searchParams.get("token");

    return (
        <PageTemplate>
            <div className={styles.auth_page}>
                <form className={styles.auth_form} onSubmit={(e) => resetPasswordConfirm(e, newPassword1.value, newPassword2.value, token, navigate)}>
                    <h1 className={styles.auth_header}>Новый пароль</h1>

                    <div>
                        <input
                            className={styles.auth_input}
                            {...newPassword1.input}
                            type="password"
                            placeholder="Новый пароль"
                        />
                        <input
                            className={styles.auth_input}
                            {...newPassword2.input}
                            type="password"
                            placeholder="Подтверждение пароля"
                        />
                    </div>

                    <div>
                        <button type="submit" className={styles.auth_submit_button}>
                            Сменить пароль
                        </button>
                    </div>

                    <div className={styles.auth_links}>
                        <a href="/registration">Регистрация</a> 
                        <a href="/login">Вход в аккаунт</a>
                    </div>
                </form>
            </div>
        </PageTemplate>
    );
};

export default PasswordResetConfirmPage;