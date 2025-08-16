import styles from "../../AuthPage.module.css";
import PageTemplate from "../../../PageTemplate/PageTemplate";
import { frontendBaseURL } from "../../../../constants";
import { useInput } from "../../../../hooks/useInput";
import { resetPassword } from "./apiPasswordResetPage";

function PasswordResetPage() {
    document.title = "Сброс пароля | Магазин";
    const email = useInput("");

    return (
        <PageTemplate>
            <div className={styles.auth_page}>
                <form className={styles.auth_form} onSubmit={(e) => resetPassword(e, email.value)}>
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
                        <a href={`${frontendBaseURL}/registration`}>Регистрация</a>
                        <a href={`${frontendBaseURL}/login`}>Вход в аккаунт</a>
                    </div>
                </form>
            </div>
        </PageTemplate>
    );
};

export default PasswordResetPage;