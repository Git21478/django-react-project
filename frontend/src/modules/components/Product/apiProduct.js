import api from "../../../api";

export const addFavorite = (productId, setProducts) => {
  api
    .post("favorites/", {
      product_id: productId,
    })
    .then((res) => {
      setProducts((prevState) => {
        return prevState.map((product) => {
          if (product.id === productId) {
            return {
              ...product,
              is_favorite: true,
              favorite_id: res.data.id,
            };
          } else {
            return product;
          }
        });
      });
    })
    .catch((error) => {
      console.error(error);
    });
};

export const deleteFavorite = (favoriteId, setProducts) => {
  api
    .delete(`favorites/${favoriteId}/`)
    .then((res) => {
      setProducts((prevState) => {
        return prevState.map((product) => {
          if (product.favorite_id === favoriteId) {
            return {
              ...product,
              is_favorite: false,
              favorite_id: null,
            };
          } else {
            return product;
          }
        });
      });
    })
    .catch((error) => {
      console.error(error);
    });
};

export const addCartProduct = (productId, setProducts) => {
  api
    .post("cart/add/", {
      product_id: productId,
    })
    .then((res) => {
      setProducts((prevState) => {
        return prevState.map((product) => {
          if (product.id === productId) {
            return {
              ...product,
              is_cart_product: true,
              cart_product_id: res.data.id,
            };
          } else {
            return product;
          }
        });
      });
    })
    .catch((error) => {
      console.error(error);
    });
};
