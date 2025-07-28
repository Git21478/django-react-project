import styles from "./ReviewCreation.module.css";
import { createReview } from "../Review/apiReview";
import { useInput } from "../../../../hooks/useInput";
import ReviewCreationInfoField from "./ReviewCreationInfoField/ReviewCreationInfoField";

function ReviewCreation({ product_id, reviewsOrdering, setReviews }) {
    const title = useInput("");
    const content = useInput("");
    const rating = useInput("");

    return (
        <div className={styles.review_creation_wrapper}>
            <form onSubmit={(e) => createReview(e, product_id, reviewsOrdering, setReviews, title, content, rating)}>
                <h2>Оставить отзыв</h2>
                
                <table>
                    <tbody>
                        <ReviewCreationInfoField
                            fieldName="Заголовок:"
                            field={title}
                            fieldId="title"
                            fieldType="text"
                        />

                        <ReviewCreationInfoField
                            fieldName="Содержание:"
                            field={content}
                            fieldId="content"
                            fieldType="textarea"
                        />

                        <ReviewCreationInfoField
                            fieldName="Оценка:"
                            field={rating}
                            fieldId="rating"
                            fieldType="number"
                        />
                    </tbody>
                </table>

                <input className={styles.review_creation_submit_button} type="submit" value="Опубликовать"/>
            </form>
        </div>
    );
};

export default ReviewCreation;