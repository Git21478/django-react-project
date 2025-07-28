import styles from "./ReviewSortBar.module.css";
import { useEffect } from "react";
import { useInput } from "../../../../hooks/useInput";
import { handleOrderingChange } from "./utilsReviewSortBar";

function ReviewSortBar({ setReviewsOrdering }) {
    const orderingType = useInput("created_at");
    const orderingDirection = useInput("ascending");

    useEffect(() => {
        handleOrderingChange(orderingType.value, orderingDirection.value, setReviewsOrdering);
    }, [orderingType.value, orderingDirection.value]);

    return (
        <div className={styles.review_sort_bar_wrapper}>
            <h2>Сортировать по:</h2>

            <select className={styles.select} {...orderingType.input}>
                <option value="created_at">По времени добавления</option>
                <option value="rating">По рейтингу</option>
            </select>

            <select className={styles.select} {...orderingDirection.input}>
                <option value="ascending">По возрастанию</option>
                <option value="descending">По убыванию</option>
            </select>
        </div>
    );
};

export default ReviewSortBar;