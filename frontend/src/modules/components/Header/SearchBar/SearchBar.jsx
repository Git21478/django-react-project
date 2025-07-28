import styles from "./SearchBar.module.css";
import { useContext } from "react";
import { getProducts } from "../../../pages/HomePage/apiHomePage";
import { AppContext } from "../../../AppProvider/AppProvider";
import { useNavigate } from "react-router-dom";
import search_icon from "../../../../assets/icons/search.png";

function SearchBar() {
    const appData = useContext(AppContext);
    const navigate = useNavigate();
    
    return (
        <div className={`${styles.search_bar} ${styles.header_element}`}>
            <input
                className={styles.search_bar_element}
                type="text"
                placeholder="Поиск"
                value={appData.search}
                onChange={(e) => appData.setSearch(e.target.value)}
            />
            <img
                className={styles.header_icon}
                src={search_icon}
                alt="Search"
                onClick={() => {
                    getProducts(appData.setProducts, appData.setProductsAmount, appData.currentPage, appData.pageSize, appData.ordering, appData.search)
                    navigate("/");
                }}
            />
        </div>
    );
};

export default SearchBar;