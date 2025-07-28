export const handleCheckboxAllCartProducts = (cart_products, selectedCartProductsIds, setSelectedCartProductsIds) => {
    if (cart_products.length === selectedCartProductsIds.length) {
        setSelectedCartProductsIds([]);
    } else {
        const cartProductIds = cart_products.map(cartProduct => {
            return cartProduct.id;
        });
        setSelectedCartProductsIds(cartProductIds);
    };
};