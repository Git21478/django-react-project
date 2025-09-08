import styles from "./HeaderLeft.module.css";
import { useContext } from "react";
import { AppContext } from "../../../AppProvider/AppProvider";

function HeaderLeft() {
    const appData = useContext(AppContext);

    return (
        <div className={`${styles.header_left} ${styles.header_element}`}>
            <h2><a className={styles.home_link} href="/">Главная</a></h2>
            <h2 className={styles.catalog_h2} onClick={() => appData.setOpenCatalog(!appData.openCatalog ? true : false)}>Каталог</h2>
        </div>
    );
};

export default HeaderLeft;