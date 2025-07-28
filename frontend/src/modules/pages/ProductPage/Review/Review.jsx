import styles from "./Review.module.css";
import { useEffect, useState } from "react";
import { getAuthorUsername, deleteReview, reviewIsAllowedCheck } from "../../../pages/ProductPage/Review/apiReview";
import { showRatingStars } from "./utilsReview.jsx";

function Review({ reviewObject, reviewsOrdering, setReviews }) {
    const [review, setReview] = useState(reviewObject);
    const [isAllowed, setIsAllowed] = useState(false);
    const formattedDate = new Date(reviewObject.created_at).toLocaleDateString("en-US");
    
    useEffect(() => {
        getAuthorUsername(review, setReview);
        reviewIsAllowedCheck(review, setIsAllowed);
    }, []);

    return (
        <div className={styles.review}>
            <div className={styles.review_title_date}>
                <h2 className={styles.review_title}>{review.title}</h2>
                <h3>{formattedDate}</h3>
            </div>
            <p>{review.content}</p>

            {showRatingStars(review.rating)}

            <div className={styles.review_buttons}>
                <span/>
                <h2>@{review.authorUsername}</h2>
                {isAllowed
                    ? <button className={styles.delete_button} onClick={() => deleteReview(review, reviewsOrdering, setReviews)}>Delete</button>
                    : <span/>
                }
            </div>
        </div>
    );
};

export default Review;