import api from "../../../../api";

export const addFavorite = (productPageProductId, setProductPageProduct) => {
  api
    .post("/api/favorites/", {
      product: productPageProductId,
    })
    .then((res) => {
      setProductPageProduct((prevState) => {
        return { ...prevState, is_favorite: true, favorite_id: res.data.id };
      });
    })
    .catch((error) => {
      console.error(error);
    });
};

export const deleteFavorite = (favoriteId, setProductPageProduct) => {
  api
    .delete(`/api/favorites/${favoriteId}/`)
    .then((res) => {
      setProductPageProduct((prevState) => {
        return { ...prevState, is_favorite: false, favorite_id: null };
      });
    })
    .catch((error) => {
      console.error(error);
    });
};

export const addCartProduct = (productPageProductId, setProductPageProduct) => {
  api
    .post("/api/cart/", {
      product: productPageProductId,
    })
    .then((res) => {
      setProductPageProduct((prevState) => {
        return {
          ...prevState,
          is_cart_product: true,
          cart_product_id: res.data.id,
        };
      });
    })
    .catch((error) => {
      console.error(error);
    });
};
