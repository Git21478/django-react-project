import styles from "./FavoritesPage.module.css";
import { useContext, useEffect, useState } from "react";
import { AppContext } from "../../AppProvider/AppProvider";
import PageTemplate from "../../PageTemplate/PageTemplate";
import { deleteMultipleFavoriteProducts, getFavoriteProducts } from "./apiFavoritesPage";
import FavoriteProduct from "./FavoriteProduct/FavoriteProduct";
import { handleCheckboxAllFavoriteProducts } from "./utilsFavoritesPage";

function FavoritesPage() {
    document.title = "Избранное | Магазин";
    const appData = useContext(AppContext);
    const [selectedFavoriteProductsIds, setSelectedFavoriteProductsIds] = useState([]);

    useEffect(() => {
        getFavoriteProducts(appData.setFavoriteProducts);
    }, []);

    useEffect(() => {
        console.log(selectedFavoriteProductsIds);
    }, [selectedFavoriteProductsIds]);

    return (
        <PageTemplate>
            <div className={styles.favorites_page_wrapper}>
                <h1 className={styles.favorites_page_header}>Избранное</h1>

                <div className={styles.favorites_page_select_section}>
                    <div className={styles.favorites_page_select_all}>
                        <input
                            type="checkbox"
                            id="checkboxAll"
                            checked={selectedFavoriteProductsIds.length === appData.favoriteProducts.length && selectedFavoriteProductsIds.length !== 0}
                            onChange={() => handleCheckboxAllFavoriteProducts(appData.favoriteProducts, selectedFavoriteProductsIds, setSelectedFavoriteProductsIds)}
                        />
                        <label htmlFor="checkboxAll"><h2>Выбрать все</h2></label>
                    </div>

                    {selectedFavoriteProductsIds.length !== 0 && 
                        <h2 onClick={() => deleteMultipleFavoriteProducts(selectedFavoriteProductsIds, setSelectedFavoriteProductsIds, appData.setFavoriteProducts)}>Удалить выбранные товары</h2>
                    }
                </div>

                <div>
                    {appData.favoriteProducts.map(favoriteProduct => (
                        <FavoriteProduct
                            favoriteProduct={favoriteProduct}
                            setFavoriteProducts={appData.setFavoriteProducts}
                            selectedFavoriteProductsIds={selectedFavoriteProductsIds}
                            setSelectedFavoriteProductsIds={setSelectedFavoriteProductsIds}
                            key={favoriteProduct.id}
                        />
                    ))}
                </div>
            </div>
        </PageTemplate>
    );
};

export default FavoritesPage;