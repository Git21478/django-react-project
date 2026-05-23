export const handleCheckboxAllCartProducts = (cart_products, selectedCartProductIds, setSelectedCartProductIds) => {
    if (cart_products.length === selectedCartProductIds.length) {
        setSelectedCartProductIds([]);
    } else {
        const cartProductIds = cart_products.map(cartProduct => {
            return cartProduct.id;
        });
        setSelectedCartProductIds(cartProductIds);
    };
};