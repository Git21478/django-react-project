import api from "../../../api";

export const getFavorites = (setFavorites) => {
  api
    .get("api/favorites/")
    .then((res) => {
      setFavorites(res.data);
    })
    .catch((error) => {
      console.error(error);
    });
};

export const deleteMultipleFavorites = (
  selectedFavoritesIds,
  setSelectedFavoritesIds,
  setFavorites,
) => {
  const idsParam = selectedFavoritesIds.join(",");

  api
    .delete(`api/favorites/delete-multiple/?ids=${idsParam}`)
    .then((res) => {
      setSelectedFavoritesIds((prevData) => {
        return prevData.filter((id) => {
          return !selectedFavoritesIds.includes(id);
        });
      });
      getFavorites(setFavorites);
    })
    .catch((error) => {
      console.error(error);
    });
};
