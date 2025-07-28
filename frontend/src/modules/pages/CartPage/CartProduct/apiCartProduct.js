import api from "../../../../api";

export const changeCartProductQuantity = (cartProductId, quantity, setCartProductsObject) => {
    api
        .patch(`/api/cart-products/${cartProductId}/`, {
            quantity,
        })
        .then((res) => {
            console.log(res.data);
            setCartProductsObject(prevState => {
                const cart_products = prevState.cart_products.map(cartProduct => {
                    if (cartProduct.id === cartProductId) {
                        return res.data;
                    };
                    return cartProduct;
                });
                return {cart_products: cart_products, total_quantity: res.data.total_quantity, total_price: res.data.total_price}
            });
        })
        .catch((error) => {
            console.log(error);
        });
};

export const addFavoriteProduct = (productId, setCartProductsObject) => {
    api
        .post("/api/favorite-products/", {
            product: productId,
        })
        .then((res) => {
            console.log(res.data);
            setCartProductsObject(prevState => {
                const cart_products = prevState.cart_products.map(cartProduct => {
                    if (cartProduct.product.id === productId) {
                        return {...cartProduct, product: {...cartProduct.product, is_favorite_product: true, favorite_product_id: res.data.id}};
                    } else {
                        return cartProduct;
                    };
                });
                return {...prevState, cart_products};
            });
        })
        .catch((error) => {
            console.log(error);
        });
};

export const deleteFavoriteProduct = (favoriteProductId, setCartProductsObject) => {
    api
        .delete(`/api/favorite-products/${favoriteProductId}/`)
        .then((res) => {
            console.log(res);
            setCartProductsObject(prevState => {
                const cart_products = prevState.cart_products.map(cartProduct => {
                    if (cartProduct.product.favorite_product_id === favoriteProductId) {
                        return {...cartProduct, product: {...cartProduct.product, is_favorite_product: false, favorite_product_id: null}};
                    } else {
                        return cartProduct;
                    };
                });
                return {...prevState, cart_products};
            });
        })
        .catch((error) => {
            console.log(error);
        });
};

export const deleteCartProduct = (cartProductId, getCartProducts, setCartProducts, setCartProductsTotalQuantity, setCartProductsTotalPrice) => {
    api
        .delete(`/api/cart-products/${cartProductId}/`)
        .then((res) => {
            console.log(res);
            getCartProducts(setCartProducts, setCartProductsTotalQuantity, setCartProductsTotalPrice);
        })
        .catch((error) => {
            console.log(error);
        });
};