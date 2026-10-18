import styles from "./SearchBar.module.css";
import { useContext } from "react";
import { AppContext } from "../../../AppProvider/AppProvider";
import { useNavigate } from "react-router-dom";
import search_icon from "../../../../assets/icons/search.png";

function SearchBar() {
  const appData = useContext(AppContext);
  const navigate = useNavigate();

  const handleSearch = () => {
    appData.applySearch();
    navigate("/");
  };

  return (
    <div className={`${styles.search_bar} ${styles.header_element}`}>
      <input
        className={styles.search_bar_element}
        type="text"
        placeholder="Поиск"
        value={appData.searchInput}
        onChange={(e) => appData.setSearchInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault();
            handleSearch();
          }
        }}
      />
      <button type="button" onClick={handleSearch} aria-label="Поиск">
        <img
          className={`${styles.header_icon} ${styles.search_bar_icon}`}
          src={search_icon}
          alt=""
        />
      </button>
    </div>
  );
}

export default SearchBar;
