import api from "../../../api";

export const getFavoriteProducts = (setFavoriteProducts) => {
    api
        .get("api/favorite-products/")
        .then((res) => {
            console.log("res.data (favorite products page)");
            console.log(res.data);
            setFavoriteProducts(res.data);
        })
        .catch((error) => {
            console.log(error);
        });
};

export const deleteMultipleFavoriteProducts = (selectedFavoriteProductsIds, setSelectedFavoriteProductsIds, setFavoriteProducts) => {
    api
        .put("api/favorite-products/delete-multiple/", {
            favoriteProductsIds: selectedFavoriteProductsIds,
        })
        .then((res) => {
            console.log(res);
            setSelectedFavoriteProductsIds(prevData => {
                return prevData.filter(id => {
                    return !selectedFavoriteProductsIds.includes(id);
                });
            });
            getFavoriteProducts(setFavoriteProducts);
        })
        .catch((error) => {
            console.log(error);
        });
};