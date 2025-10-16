import api from "../../../../api";
import { getReviews } from "../apiProductPage";

export const reviewIsAllowedCheck = (review, setIsAllowed) => {
    api
        .get("/api/user/")
        .then((res) => {
            const userId = res.data[0].id;
            if (userId === review.author) {
                setIsAllowed(true);
            };
        })
        .catch((err) => console.log(err));
};

export const createReview = (e, product_id, reviewsOrdering, setReviews, title, content, rating) => {
    e.preventDefault();
    api
        .post(`/api/products/${product_id}/reviews/`, {
            title: title.value,
            content: content.value,
            rating: rating.value,
            product: product_id,
        })
        .then((res) => {
            if (res.status === 201) console.log("Review created.");
            else console.log("Failed to make review.");
            getReviews(product_id, reviewsOrdering, setReviews);
        })
        .catch((error) => console.log(error))
        .finally(() => {
            title.clear();
            content.clear();
            rating.clear();
        });
};

export const changeReview = (review, setReviews) => {
    api
        .put(`/api/products/reviews/${review.id}/`, {
            title: review.title,
            content: review.content,
            rating: review.rating,
            product: review.product,
        })
        .then((res) => {
            if (res.status === 200) console.log("Review changed.");
            else console.log("Failed to change review.");
            getReviews(setReviews, review.product);
        })
        .catch((error) => console.log(error));
};

export const deleteReview = (review, reviewsOrdering, setReviews) => {
    console.log("review.product");
    console.log(review.product);
    api
        .delete(`/api/products/reviews/${review.id}/`)
        .then((res) => {
            if (res.status === 204) console.log ("Review deleted.");
            else console.log("Failed to delete review.");
            getReviews(review.product, reviewsOrdering, setReviews);
        })
        .catch((error) => console.log(error));
};