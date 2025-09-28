import api from "../../../../api";

export const addFavoriteProduct = (productPageProductId, setProductPageProduct) => {
    api
        .post("/api/favorite-products/", {
            product: productPageProductId,
        })
        .then((res) => {
            console.log(res.data);
            setProductPageProduct(prevState => {
                return {...prevState, is_favorite_product: true, favorite_product_id: res.data.id};
            });
        })
        .catch((error) => {
            console.log(error);
        });
};

export const deleteFavoriteProduct = (favoriteProductId, setProductPageProduct) => {
    api
        .delete(`/api/favorite-products/${favoriteProductId}/`)
        .then((res) => {
            console.log(res);
            setProductPageProduct(prevState => {
                return {...prevState, is_favorite_product: false, favorite_product_id: null};
            });
        })
        .catch((error) => {
            console.log(error);
        });
};

export const addCartProduct = (productPageProductId, setProductPageProduct) => {
    api
        .post(`/api/cart-products/`, {
            product: productPageProductId,
        })
        .then((res) => {
            console.log(res.data);
            setProductPageProduct(prevState => {
                return {...prevState, is_cart_product: true, cart_product_id: res.data.id};
            });
        })
        .catch((error) => {
            console.log(error);
        });
};