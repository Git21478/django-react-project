import api from "../../../api";

export const addFavoriteProduct = (productId, setProducts) => {
    api
        .post("/api/favorite-products/", {
            product: productId,
        })
        .then((res) => {
            console.log(res.data);
            setProducts(prevState => {
                return prevState.map(product => {
                    if (product.id === productId) {
                        return {...product, is_favorite_product: true, favorite_product_id: res.data.id};
                    } else {
                        return product;
                    };
                });
            });
        })
        .catch((error) => {
            console.log(error);
        });
};

export const deleteFavoriteProduct = (favoriteProductId, setProducts) => {
    api
        .delete(`/api/favorite-products/${favoriteProductId}/`)
        .then((res) => {
            console.log(res);
            setProducts(prevState => {
                return prevState.map(product => {
                    if (product.favorite_product_id === favoriteProductId) {
                        return {...product, is_favorite_product: false, favorite_product_id: null};
                    } else {
                        return product;
                    };
                });
            });
        })
        .catch((error) => {
            console.log(error);
        });
};

export const addCartProduct = (productId, setProducts) => {
    api
        .post(`/api/cart-products/`, {
            product: productId,
        })
        .then((res) => {
            console.log(res.data);
            setProducts(prevState => {
                return prevState.map(product => {
                    if (product.id === productId) {
                        return {...product, is_cart_product: true, cart_product_id: res.data.id};
                    } else {
                        return product;
                    };
                });
            });
        })
        .catch((error) => {
            console.log(error);
        });
};