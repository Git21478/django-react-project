import api from "../../../../api";

export const handleCheckout = (cartProducts, setCartProductsObject, setSelectedCartProductsIds) => {
    const cartProductsIds = cartProducts.map(cartProduct => {
        return cartProduct.id;
    });

    api
        .put("api/cart-products/delete-multiple/", {
            cartProductsIds,
        })
        .then((res) => {
            console.log(res);
            setSelectedCartProductsIds([]);
            setCartProductsObject({cart_products: [], total_quantity: 0, total_price: 0});
            alert("Заказ оформлен");
        })
        .catch((error) => {
            console.log(error);
        });
};