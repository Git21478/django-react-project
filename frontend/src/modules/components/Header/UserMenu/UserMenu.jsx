import styles from "./UserMenu.module.css";
import { useContext } from "react";
import { backendBaseURL } from "../../../../constants";
import { AppContext } from "../../../AppProvider/AppProvider";
import admin_panel_icon from "../../../../assets/icons/admin_panel.png";
import profile_icon from "../../../../assets/icons/profile.png";
import login_icon from "../../../../assets/icons/login.png";
import logout_icon from "../../../../assets/icons/logout.png";
import registration_icon from "../../../../assets/icons/registration.png";
import { Link } from "react-router-dom";

function UserMenu() {
  const appData = useContext(AppContext);

  return (
    <div className={styles.user_menu_wrapper}>
      {appData.openUserMenu && (
        <>
          {appData.isAuthenticated && (
            <ul>
              <li className={styles.user_menu_section}>
                <img
                  className={styles.user_menu_section_icon}
                  src={profile_icon}
                  alt="user menu section icon"
                />
                <Link to="/profile">Профиль</Link>
              </li>
              <li className={styles.user_menu_section}>
                <img
                  className={styles.user_menu_section_icon}
                  src={admin_panel_icon}
                  alt="user menu section icon"
                />
                <Link to={`${backendBaseURL}/admin`} target="_blank">
                  Админ панель
                </Link>
              </li>
              <li className={styles.user_menu_section}>
                <img
                  className={styles.user_menu_section_icon}
                  src={logout_icon}
                  alt="user menu section icon"
                />
                <Link to="/logout">Выйти</Link>
              </li>
            </ul>
          )}

          {!appData.isAuthenticated && (
            <ul>
              <li className={styles.user_menu_section}>
                <img
                  className={styles.user_menu_section_icon}
                  src={login_icon}
                  alt="user menu section icon"
                />
                <Link to="/login">Вход</Link>
              </li>
              <li className={styles.user_menu_section}>
                <img
                  className={styles.user_menu_section_icon}
                  src={admin_panel_icon}
                  alt="user menu section icon"
                />
                <Link to="/admin" target="_blank">
                  Админ панель
                </Link>
              </li>
              <li className={styles.user_menu_section}>
                <img
                  className={styles.user_menu_section_icon}
                  src={registration_icon}
                  alt="user menu section icon"
                />
                <Link to="/registration">Регистрация</Link>
              </li>
            </ul>
          )}
        </>
      )}
    </div>
  );
}

export default UserMenu;
