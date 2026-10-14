import api from "../../../../api";

export const deleteFavorite = (favoriteId, setFavorites) => {
  api
    .delete(`favorites/${favoriteId}/`)
    .then((res) => {
      setFavorites((prevState) => {
        const favorites = prevState.filter((favorite) => {
          return favorite.id !== favoriteId;
        });
        return favorites;
      });
    })
    .catch((error) => {
      console.error(error);
    });
};

export const addCartProduct = (product_id, setFavorites) => {
  api
    .post("cart/add/", {
      product_id: product_id,
    })
    .then((res) => {
      setFavorites((prevState) => {
        return prevState.map((favorite) => {
          if (favorite.product.id === product_id) {
            return {
              ...favorite,
              product: {
                ...favorite.product,
                is_cart_product: true,
                cart_product_id: res.data.id,
              },
            };
          } else {
            return favorite;
          }
        });
      });
    })
    .catch((error) => {
      console.error(error);
    });
};
