import styles from "./SearchBar.module.css";
import { useContext, useEffect, useRef } from "react";
import { getProducts } from "../../../pages/HomePage/apiHomePage";
import { AppContext } from "../../../AppProvider/AppProvider";
import { useNavigate } from "react-router-dom";
import search_icon from "../../../../assets/icons/search.png";

function SearchBar() {
    const appData = useContext(AppContext);
    const navigate = useNavigate();
    const searchInputRef = useRef(null);
    const searchButtonRef = useRef(null);

    useEffect(() => {
        searchInputRef.current.addEventListener("keyup", (event) => {
            event.preventDefault();
            if (event.key === "Enter") {
                searchButtonRef.current.click();
            };
        });
    }, []);
    
    return (
        <div className={`${styles.search_bar} ${styles.header_element}`}>
            <input
                className={styles.search_bar_element}
                type="text"
                placeholder="Поиск"
                value={appData.search}
                onChange={(e) => appData.setSearch(e.target.value)}
                ref={searchInputRef}
            />
            <img
                className={styles.header_icon}
                src={search_icon}
                alt="Search"
                onClick={() => {
                    getProducts(appData.setProducts, appData.setProductsAmount, appData.currentPage, appData.pageSize, appData.ordering, appData.search)
                    navigate("/");
                }}
                ref={searchButtonRef}
            />
        </div>
    );
};

export default SearchBar;