export const handleCheckboxAllFavorites = (
  favorites,
  selectedFavoritesIds,
  setSelectedFavoritesIds,
) => {
  if (favorites.length === selectedFavoritesIds.length) {
    setSelectedFavoritesIds([]);
  } else {
    const selectedFavoritesIds = favorites.map((favorite) => {
      return favorite.id;
    });
    setSelectedFavoritesIds(selectedFavoritesIds);
  }
};
