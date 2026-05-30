import api from "../../../../api";

export const createReview = (e, product_id, reviewsOrdering, setReviews, title, content, rating) => {
    e.preventDefault();
    api
        .post(`/api/products/${product_id}/reviews/`, {
            title: title.value,
            content: content.value,
            rating: rating.value,
        })
        .then((res) => {
            if (res.status === 201) console.log("Review created.");
            else console.log("Failed to make review.");
            setReviews(res.data);
        })
        .catch((error) => {
            console.log(error);
            alert("Вы уже оставляли отзыв на данный товар");
        })
        .finally(() => {
            title.clear();
            content.clear();
            rating.clear();
        });
};

export const deleteReview = (review, reviewsOrdering, setReviews) => {
    api
        .delete(`/api/products/reviews/${review.id}/`)
        .then((res) => {
            console.log(res);
            if (res.status === 200) console.log ("Review deleted.");
            else console.log("Failed to delete review.");
            setReviews(res.data);
        })
        .catch((error) => console.log(error));
};