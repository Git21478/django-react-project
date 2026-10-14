import api from "../../../../api";

export const changeCartProductQuantity = (product_id, quantity, setCart) => {
  api
    .patch(`cart/update/${product_id}/`, {
      quantity,
    })
    .then((res) => {
      setCart(res.data);
    })
    .catch((error) => {
      console.error(error);
    });
};

export const addFavorite = (product_id, setCart) => {
  api
    .post("favorites/", {
      product_id,
    })
    .then((res) => {
      setCart((prevState) => {
        const cart_products = prevState.cart_products.map((cartProduct) => {
          if (cartProduct.product.id === product_id) {
            return {
              ...cartProduct,
              product: {
                ...cartProduct.product,
                is_favorite: true,
                favorite_id: res.data.id,
              },
            };
          } else {
            return cartProduct;
          }
        });
        return { ...prevState, cart_products };
      });
    })
    .catch((error) => {
      console.error(error);
    });
};

export const deleteFavorite = (favoriteId, setCart) => {
  api
    .delete(`favorites/${favoriteId}/`)
    .then((res) => {
      setCart((prevState) => {
        const cart_products = prevState.cart_products.map((cartProduct) => {
          if (cartProduct.product.favorite_id === favoriteId) {
            return {
              ...cartProduct,
              product: {
                ...cartProduct.product,
                is_favorite: false,
                favorite_id: null,
              },
            };
          } else {
            return cartProduct;
          }
        });
        return { ...prevState, cart_products };
      });
    })
    .catch((error) => {
      console.error(error);
    });
};

export const deleteCartProduct = (product_id, setCart) => {
  api
    .delete(`cart/remove/${product_id}/`)
    .then((res) => {
      setCart(res.data);
    })
    .catch((error) => {
      console.error(error);
    });
};
