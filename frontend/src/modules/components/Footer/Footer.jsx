import styles from "./Footer.module.css";

function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className={styles.footer_container}>
            <h2>&copy; {currentYear} DJANGOSTORE</h2>
        </footer>
    );
};

export default Footer;