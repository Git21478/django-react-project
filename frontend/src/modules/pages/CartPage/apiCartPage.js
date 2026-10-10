import api from "../../../api";

export const getCart = (setCart) => {
  api
    .get("api/cart/")
    .then((res) => {
      setCart(res.data);
    })
    .catch((error) => {
      console.error(error);
    });
};

export const deleteMultipleCartProducts = (
  selectedCartProductIds,
  setSelectedCartProductIds,
  setCart,
) => {
  api
    .delete("api/cart/delete-multiple/", {
      data: {
        cart_product_ids: selectedCartProductIds,
      },
    })
    .then((res) => {
      setSelectedCartProductIds([]);

      if (res.data) {
        setCart(res.data);
      }
      getCart(setCart);
    })
    .catch((error) => {
      console.error(error);
    });
};
