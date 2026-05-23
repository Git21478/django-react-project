import api from "../../../api";

export const getFavorites = (setFavorites) => {
    api
        .get("api/favorites/")
        .then((res) => {
            console.log("res.data (favorite products page)");
            console.log(res.data);
            setFavorites(res.data);
        })
        .catch((error) => {
            console.log(error);
        });
};

export const deleteMultipleFavorites = (selectedFavoritesIds, setSelectedFavoritesIds, setFavorites) => {
    const idsParam = selectedFavoritesIds.join(",");

    api
        .delete(`api/favorites/delete-multiple/?ids=${idsParam}`)
        .then((res) => {
            console.log(res);
            setSelectedFavoritesIds(prevData => {
                return prevData.filter(id => {
                    return !selectedFavoritesIds.includes(id);
                });
            });
            getFavorites(setFavorites);
        })
        .catch((error) => {
            console.log(error);
        });
};