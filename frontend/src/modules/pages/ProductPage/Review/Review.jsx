import styles from "./Review.module.css";
import { useEffect, useState } from "react";
import { deleteReview, reviewIsAllowedCheck } from "../../../pages/ProductPage/Review/apiReview";
import { showRatingStars } from "./utilsReview.jsx";

function Review({ review, reviewsOrdering, setReviews }) {
    const [isAllowed, setIsAllowed] = useState(false);
    const formattedDate = new Date(review.created_at).toLocaleDateString("en-US");
    
    useEffect(() => {
        reviewIsAllowedCheck(review, setIsAllowed);
    }, []);

    return (
        <div className={styles.review}>
            <div className={styles.review_title_date}>
                <h2 className={styles.review_title}>{review.title}</h2>
                <h3 className={styles.author_username}>@{review.author}</h3>
            </div>

            <p>{review.content}</p>

            <div className={styles.review_bottom}>
                <div className={styles.rating_stars}>
                    {showRatingStars(review.rating)}
                </div>

                <div className={styles.review_bottom_right}>
                    {isAllowed && <button className={styles.delete_button} onClick={() => deleteReview(review, reviewsOrdering, setReviews)}>Удалить</button>}
                    <h4>{formattedDate}</h4>
                </div>
            </div>
        </div>
    );
};

export default Review;