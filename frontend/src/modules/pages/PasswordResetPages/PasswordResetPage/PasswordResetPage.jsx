import styles from "../../AuthPage.module.css";
import { frontendBaseURL } from "../../../../constants";
import { useInput } from "../../../../hooks/useInput";
import { resetPassword } from "./apiPasswordResetPage";
import { useState } from "react";
import PageTemplate from "../../../PageTemplate/PageTemplate";

function PasswordResetPage() {
    document.title = "Сброс пароля | Магазин";
    const email = useInput("");
    const [csrftoken, setCsrftoken] = useState("");

    const setCookie = (name, value, daysToLive) => {
        const date = new Date();
        date.setTime(date.getTime() + (daysToLive * 24 * 60 * 60 * 1000));
        let expires = "expires=" + date.toUTCString();
        document.cookie = `${name}=${value}; ${expires}; path=/`;
    };

    const deleteCookie = (name) => {
        setCookie(name, null, null);
        console.log("Delete", name);
    };

    const getCookie = (name) => {
        const cookieDecoded = decodeURIComponent(document.cookie);
        const cookieArray = cookieDecoded.split("; ");
        let result = null;

        cookieArray.forEach(el => {
            if (el.indexOf(name) == 0) {
                result = el.substring(name.length + 1);
            };
        });

        console.log("result");
        console.log(result);
    };

    return (
        <PageTemplate>
            <div className={styles.auth_page}>
                <form className={styles.auth_form} onSubmit={(e) => resetPassword(e, email)}>
                    <h1 className={styles.auth_header}>Сброс пароля {csrftoken}</h1>

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

                {/* <button onClick={() => setCookie("email", "Sponge@gmail.com", 365)}>Set Cookie</button>
                <button onClick={() => deleteCookie("email")}>Delete Cookie</button>
                <button onClick={() => getCookie("csrftoken")}>Get Cookie</button> */}
            </div>
        </PageTemplate>
    );
};

export default PasswordResetPage;