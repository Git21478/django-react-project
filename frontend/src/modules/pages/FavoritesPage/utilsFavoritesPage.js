export const handleCheckboxAllFavoriteProducts = (favoriteProducts, selectedFavoriteProductsIds, setSelectedFavoriteProductsIds) => {
    if (favoriteProducts.length === selectedFavoriteProductsIds.length) {
        setSelectedFavoriteProductsIds([]);
    } else {
        const selectedFavoriteProductsIds = favoriteProducts.map(favoriteProduct => {
            return favoriteProduct.id;
        });
        setSelectedFavoriteProductsIds(selectedFavoriteProductsIds);
    };
};