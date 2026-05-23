import api from "../../../api";

export const addFavorite = (productId, setProducts) => {
    api
        .post("/api/favorites/", {
            product_id: productId,
        })
        .then((res) => {
            console.log(res.data);
            setProducts(prevState => {
                return prevState.map(product => {
                    if (product.id === productId) {
                        return {...product, is_favorite: true, favorite_id: res.data.id};
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

export const deleteFavorite = (favoriteId, setProducts) => {
    api
        .delete(`/api/favorites/${favoriteId}/`)
        .then((res) => {
            console.log(res);
            setProducts(prevState => {
                return prevState.map(product => {
                    if (product.favorite_id === favoriteId) {
                        return {...product, is_favorite: false, favorite_id: null};
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
        .post("/api/cart/add/", {
            product_id: productId,
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