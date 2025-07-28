import styles from "./UserMenu.module.css";
import { useContext } from "react";
import { backendBaseURL, frontendBaseURL } from "../../../../constants";
import { AppContext } from "../../../AppProvider/AppProvider";
import bell from "../../../../assets/icons/bell.png";
import login_icon from "../../../../assets/icons/login.png";
import registration_icon from "../../../../assets/icons/registration.png";

function UserMenu() {
    const appData = useContext(AppContext);
    
    return (
        <div className={styles.user_menu_wrapper}>
            {appData.openUserMenu && (
                <>
                    {appData.isAuthenticated && (
                        <ul>
                            <li className={styles.user_menu_section}>
                                <img className={styles.user_menu_section_icon} src={bell} alt="user menu section icon" />
                                <a href={`${frontendBaseURL}/profile`}>Профиль</a>
                            </li>
                            <li className={styles.user_menu_section}>
                                <img className={styles.user_menu_section_icon} src={bell} alt="user menu section icon" />
                                <a href={`${backendBaseURL}/admin`} target="_blank">Админ панель</a>
                            </li>
                            {/* <li className={styles.user_menu_section}>
                                <img className={styles.user_menu_section_icon} src={bell} alt="user menu section icon" />
                                <a href={`${frontendBaseURL}/admin-panel`}>Админ панель API</a>
                            </li> */}
                            <li className={styles.user_menu_section}>
                                <img className={styles.user_menu_section_icon} src={bell} alt="user menu section icon" />
                                <a href={`${frontendBaseURL}/logout`}>Выйти</a>
                            </li>
                        </ul>
                    )}

                    {!appData.isAuthenticated && (
                        <ul>
                            <li className={styles.user_menu_section}>
                                <img className={styles.user_menu_section_icon} src={login_icon} alt="user menu section icon" />
                                <a href={`${frontendBaseURL}/login`}>Вход</a>
                            </li>
                            <li className={styles.user_menu_section}>
                                <img className={styles.user_menu_section_icon} src={registration_icon} alt="user menu section icon" />
                                <a href={`${frontendBaseURL}/registration`}>Регистрация</a>
                            </li>
                        </ul>
                    )}
                </>
            )}
        </div>
    );
};

export default UserMenu;