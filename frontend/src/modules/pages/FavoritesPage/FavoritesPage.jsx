import styles from "./FavoritesPage.module.css";
import { useContext, useEffect, useState } from "react";
import { AppContext } from "../../AppProvider/AppProvider";
import PageTemplate from "../../PageTemplate/PageTemplate";
import { deleteMultipleFavorites, getFavorites } from "./apiFavoritesPage";
import Favorite from "./Favorite/Favorite";
import { handleCheckboxAllFavorites } from "./utilsFavoritesPage";

function FavoritesPage() {
  document.title = "Избранное | Магазин";
  const appData = useContext(AppContext);
  const [selectedFavoritesIds, setSelectedFavoritesIds] = useState([]);

  useEffect(() => {
    getFavorites(appData.setFavorites);
  }, []);

  useEffect(() => {
    console.log(selectedFavoritesIds);
  }, [selectedFavoritesIds]);

  return (
    <PageTemplate>
      <div className={styles.favorites_page_wrapper}>
        <h1 className={styles.favorites_page_header}>Избранное</h1>

        <div className={styles.favorites_page_select_section}>
          <div className={styles.favorites_page_select_all}>
            <input
              type="checkbox"
              id="checkboxAll"
              checked={
                selectedFavoritesIds.length === appData.favorites.length &&
                selectedFavoritesIds.length !== 0
              }
              onChange={() =>
                handleCheckboxAllFavorites(
                  appData.favorites,
                  selectedFavoritesIds,
                  setSelectedFavoritesIds,
                )
              }
            />
            <label htmlFor="checkboxAll">
              <h2>Выбрать все</h2>
            </label>
          </div>

          {selectedFavoritesIds.length !== 0 && (
            <h2
              onClick={() =>
                deleteMultipleFavorites(
                  selectedFavoritesIds,
                  setSelectedFavoritesIds,
                  appData.setFavorites,
                )
              }
            >
              Удалить выбранные товары
            </h2>
          )}
        </div>

        <div>
          {appData.favorites.map((favorite) => (
            <Favorite
              favorite={favorite}
              setFavorites={appData.setFavorites}
              selectedFavoritesIds={selectedFavoritesIds}
              setSelectedFavoritesIds={setSelectedFavoritesIds}
              key={favorite.id}
            />
          ))}
        </div>
      </div>
    </PageTemplate>
  );
}

export default FavoritesPage;
