import styles from "./SortBarCenter.module.css";
import { useEffect } from "react";
import { useInput } from "../../../hooks/useInput";
import { handleOrderingChange } from "./utilsSortBarCenter";

function SortBarCenter({ setProductsOrdering }) {
    const productsOrderingType = useInput("price");
    const productsOrderingDirection = useInput("ascending");

    useEffect(() => {
        handleOrderingChange(productsOrderingType.value, productsOrderingDirection.value, setProductsOrdering);
    }, [productsOrderingType.value, productsOrderingDirection.value]);

    return (
        <div className={styles.sort_bar_center_wrapper}>
            <h2>Сортировать по:</h2>

            <select className={styles.select} {...productsOrderingType.input}>
                <option value="price">По цене</option>
                <option value="favorite_product_id">По сердечку</option>
                <option value="rating">По рейтингу</option>
            </select>

            <select className={styles.select} {...productsOrderingDirection.input}>
                <option value="ascending">По возрастанию</option>
                <option value="descending">По убыванию</option>
            </select>
        </div>
    );
};

export default SortBarCenter;