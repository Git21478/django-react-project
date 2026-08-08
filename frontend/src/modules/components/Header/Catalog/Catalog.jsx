import styles from "./Catalog.module.css";
import { useContext } from "react";
import { AppContext } from "../../../AppProvider/AppProvider";
import { Link } from "react-router-dom";

function Catalog() {
  const appData = useContext(AppContext);

  return (
    <div className={styles.catalog_wrapper}>
      {appData.openCatalog && (
        <ul>
          {appData.categories
            .sort((a, b) => a.id - b.id)
            .map((category) => {
              return (
                <li className={styles.category} key={category.id}>
                  <Link to={`/catalog/${category.slug}`}>{category.name}</Link>
                </li>
              );
            })}
        </ul>
      )}
    </div>
  );
}

export default Catalog;
