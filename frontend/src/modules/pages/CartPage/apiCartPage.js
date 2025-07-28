import api from "../../../api";

export const getCartProducts = (setCartProductsObject) => {
    api
        .get("api/cart-products/")
        .then((res) => {
            console.log("res.data (cartpage)");
            console.log(res.data);
            setCartProductsObject(res.data);
        })
        .catch((error) => {
            console.log(error);
        });
};

export const deleteMultipleCartProducts = (selectedCartProductsIds, setSelectedCartProductsIds, setCartProductsObject) => {
    api
        .put("api/cart-products/delete-multiple/", {
            cartProductsIds: selectedCartProductsIds,
        })
        .then((res) => {
            console.log(res);
            setSelectedCartProductsIds(prevData => {
                return prevData.filter(id => {
                    return !selectedCartProductsIds.includes(id);
                });
            });
            getCartProducts(setCartProductsObject);
        })
        .catch((error) => {
            console.log(error);
        });
};