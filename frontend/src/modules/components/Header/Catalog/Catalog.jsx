import styles from "./Catalog.module.css";
import { useContext } from "react";
import { AppContext } from "../../../AppProvider/AppProvider";

function Catalog() {
    const appData = useContext(AppContext);

    return (
        <div className={styles.catalog_wrapper}>
            {appData.openCatalog && (
                <ul>
                    {appData.categories.sort((a, b) => a.id - b.id).map(category => {
                        return (
                            <li className={styles.category} key={category.id}>
                                <a href={`/catalog/${category.slug}`}>{category.name}</a>
                            </li>
                        )
                    })}
                </ul>
            )}
        </div>
    );
};

export default Catalog;