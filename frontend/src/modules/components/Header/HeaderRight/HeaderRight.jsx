import styles from "./HeaderRight.module.css";
import { useContext } from "react";
import { AppContext } from "../../../AppProvider/AppProvider.jsx";
import favorites_1_icon from "../../../../assets/icons/favorites_1.png";
import cart_icon from "../../../../assets/icons/cart.png";
import default_avatar from "../../../../assets/icons/default_avatar.png";
import { frontendBaseURL } from "../../../../constants.js";

function HeaderRight() {
    const appData = useContext(AppContext);

    return (
        <div className={`${styles.header_right} ${styles.header_element}`}>
            <a href={`${frontendBaseURL}/favorites`}><img className={`${styles.header_icon} ${styles.header_favorites_icon}`} src={favorites_1_icon} alt="Favorites"/></a>
            <a href={`${frontendBaseURL}/cart`}><img className={styles.header_icon} src={cart_icon} alt="Cart"/></a>
            <img className={`${styles.header_icon} ${styles.header_avatar_icon}`} src={appData.avatar ? appData.avatar : default_avatar} alt="Avatar" onClick={() => appData.setOpenUserMenu(!appData.openUserMenu ? true : false)}/>
        </div>
    );
};

export default HeaderRight;