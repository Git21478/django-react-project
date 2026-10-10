import api from "../../../../api";

export const createReview = (
  e,
  product_id,
  reviewsOrdering,
  setReviews,
  title,
  content,
  rating,
) => {
  e.preventDefault();
  api
    .post(`/api/products/${product_id}/reviews/`, {
      title: title.value,
      content: content.value,
      rating: rating.value,
    })
    .then((res) => {
      setReviews(res.data);
    })
    .catch((error) => {
      console.error(error);
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
      setReviews(res.data);
    })
    .catch((error) => console.error(error));
};
