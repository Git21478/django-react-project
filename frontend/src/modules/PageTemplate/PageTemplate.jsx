import styles from "./PageTemplate.module.css";
import Header from "../components/Header/Header";
import Footer from "../components/Footer/Footer";
import Catalog from "../components/Header/Catalog/Catalog";
import UserMenu from "../components/Header/UserMenu/UserMenu";

function PageTemplate({ children }) {
    return (
        <div className={styles.page_wrapper}>
            <Header/>

            <Catalog/>
            <UserMenu/>

            {children}

            <Footer/>
        </div>
    );
};

export default PageTemplate;