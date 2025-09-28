import api from "../../../api";

export const getUserId = (setUserId) => {
    api
        .get("/api/users/")
        .then((res) => {
            setUserId(res.data[0].id);
        })
        .catch((err) => console.log(err));
};

export const getProductPageProduct = (productPageProductId, setProductPageProduct) => {
    api
        .get(`/api/products/${productPageProductId}/`)
        .then((res) => {
            console.log(res.data);
            setProductPageProduct(res.data);
        })
        .catch((err) => console.log(err));
};

export const getReviews = (productPageProductId, reviewsOrdering, setReviews) => {
    api
        .get(`/api/products/${productPageProductId}/reviews/?ordering=${reviewsOrdering}`)
        .then((res) => {
            console.log(res.data.results);
            setReviews(res.data.results);
        })
        .catch((err) => console.log(err));
};