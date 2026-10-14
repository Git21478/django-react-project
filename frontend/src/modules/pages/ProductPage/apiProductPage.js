import api from "../../../api";

export const getProductPageProduct = (
  productPageProductId,
  setProductPageProduct,
) => {
  api
    .get(`products/${productPageProductId}/`)
    .then((res) => {
      setProductPageProduct(res.data);
    })
    .catch((error) => console.error(error));
};

export const getReviews = (
  productPageProductId,
  reviewsOrdering,
  setReviews,
) => {
  api
    .get(
      `products/${productPageProductId}/reviews/?ordering=${reviewsOrdering}`,
    )
    .then((res) => {
      setReviews(res.data.results);
    })
    .catch((error) => console.error(error));
};
