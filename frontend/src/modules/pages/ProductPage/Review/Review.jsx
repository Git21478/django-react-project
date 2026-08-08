import styles from "./Review.module.css";
import { useEffect, useState } from "react";
import { deleteReview } from "../../../pages/ProductPage/Review/apiReview";
import { showRatingStars } from "./utilsReview.jsx";
import delete_icon from "../../../../assets/icons/delete.png";

function Review({ review, userId, reviewsOrdering, setReviews }) {
  const [isAllowed, setIsAllowed] = useState(false);
  const formattedDate = new Date(review.created_at).toLocaleDateString("en-US");

  useEffect(() => {
    setIsAllowed(review.author_id === userId);
  }, [userId]);

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
          <h3 className={styles.date}>{formattedDate}</h3>
        </div>

        <div className={styles.review_bottom_right}>
          {isAllowed && (
            <img
              className={styles.delete_icon}
              src={delete_icon}
              alt="Delete icon"
              onClick={() => deleteReview(review, reviewsOrdering, setReviews)}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default Review;
