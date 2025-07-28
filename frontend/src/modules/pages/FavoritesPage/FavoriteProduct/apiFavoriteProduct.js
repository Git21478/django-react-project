import api from "../../../../api";

export const deleteFavoriteProduct = (favoriteProductId, setFavoriteProducts) => {
    api
        .delete(`/api/favorite-products/${favoriteProductId}/`)
        .then((res) => {
            console.log(res);
            setFavoriteProducts(prevState => {
                const favoriteProducts = prevState.filter(favoriteProduct => {
                    if (favoriteProduct.id !== favoriteProductId) {
                        return favoriteProduct;
                    };
                });
                return favoriteProducts;
            });
        })
        .catch((error) => {
            console.log(error);
        });
};

export const addCartProduct = (productId, setFavoriteProducts) => {
    api
        .post(`/api/cart-products/`, {
            product: productId,
        })
        .then((res) => {
            console.log(res);
            setFavoriteProducts(prevState => {
                return prevState.map(favoriteProduct => {
                    if (favoriteProduct.product.id === productId) {
                        return {...favoriteProduct, product: {...favoriteProduct.product, is_cart_product: true, cart_product_id: res.data.id}};
                    } else {
                        return favoriteProduct;
                    };
                });
            });
        })
        .catch((error) => {
            console.log(error);
        });
};