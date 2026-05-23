import api from "../../../../api";

export const deleteFavorite = (favoriteId, setFavorites) => {
    api
        .delete(`/api/favorites/${favoriteId}/`)
        .then((res) => {
            console.log(res);
            setFavorites(prevState => {
                const favorites = prevState.filter(favorite => {
                    return favorite.id !== favoriteId;
                });
                return favorites;
            });
        })
        .catch((error) => {
            console.log(error);
        });
};

export const addCartProduct = (productId, setFavorites) => {
    api
        .post("/api/cart/", {
            product: productId,
        })
        .then((res) => {
            console.log(res);
            setFavorites(prevState => {
                return prevState.map(favorite => {
                    if (favorite.product.id === productId) {
                        return {...favorite, product: {...favorite.product, is_cart_product: true, cart_product_id: res.data.id}};
                    } else {
                        return favorite;
                    };
                });
            });
        })
        .catch((error) => {
            console.log(error);
        });
};