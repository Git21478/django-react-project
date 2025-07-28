import styles from "./Header.module.css";
import SearchBar from "./SearchBar/SearchBar.jsx";
import HeaderRight from "./HeaderRight/HeaderRight.jsx";
import HeaderLeft from "./HeaderLeft/HeaderLeft.jsx";

function Header() {
    return (
        <header className={styles.header_wrapper}>
            <HeaderLeft/>

            <SearchBar/>

            <HeaderRight/>
        </header>
    );
};

export default Header;