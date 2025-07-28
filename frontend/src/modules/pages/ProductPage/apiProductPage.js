import api from "../../../api";

export const getUserId = (setUserId) => {
    api
        .get("/api/users/")
        .then((res) => {
            setUserId(res.data[0].id);
        })
        .catch((err) => console.log(err));
};

export const getProduct = (productId, setProduct) => {
    api
        .get(`/api/products/${productId}/`)
        .then((res) => {
            console.log(res.data);
            setProduct(res.data);
        })
        .catch((err) => console.log(err));
};

export const getReviews = (productId, reviewsOrdering, setReviews) => {
    api
        .get(`/api/products/${productId}/reviews/?reviewsOrdering=${reviewsOrdering}`)
        .then((res) => {
            console.log(res.data.results);
            setReviews(res.data.results);
        })
        .catch((err) => console.log(err));
};