import styles from "./SortBarLeft.module.css";
import { getCurrentCategoryBrands } from "./apiSortBarLeft";
import { useContext, useEffect, useState } from "react";
import { useInput } from "../../../hooks/useInput";
import { AppContext } from "../../AppProvider/AppProvider";
import { getProducts } from "../../AppProvider/apiAppProvider";
import {
  handleCheckboxChange,
  applyFilters,
  clearFilters,
} from "./utilsSortBarLeft";

function SortBarLeft() {
  const appData = useContext(AppContext);
  const priceMin = useInput("");
  const priceMax = useInput("");
  const [brands, setBrands] = useState([]);

  useEffect(() => {
    if (appData.currentCategory) {
      getCurrentCategoryBrands(appData.currentCategory, setBrands);
    } else {
      setBrands([]);
    }
  }, [appData.currentCategory?.id]);

  if (!appData.currentCategory) {
    return null;
  }

  return (
    <div className={styles.sort_bar_left_wrapper}>
      <h1 className={styles.product_sort_menu_header}>
        {appData.currentCategory.name}
      </h1>

      <div>
        <div className={styles.filter_element}>
          <h2>Цена</h2>
          <input type="text" placeholder="от" {...priceMin.input} />
          <input type="text" placeholder="до" {...priceMax.input} />
        </div>

        <div className={styles.filter_element}>
          <h2>Производитель</h2>
          <div>
            {brands.map((brand) => {
              return (
                <div key={brand.id}>
                  <label>
                    <input
                      type="checkbox"
                      checked={brand.checked}
                      onChange={() => handleCheckboxChange(brand.id, setBrands)}
                    />
                    {brand.name}
                  </label>
                </div>
              );
            })}
          </div>
        </div>

        <div className={styles.filter_element}>
          <input
            type="submit"
            value="Применить"
            onClick={() => {
              applyFilters({
                getProducts,
                appData,
                priceMin: priceMin.value,
                priceMax: priceMax.value,
                brandIds: brands
                  .filter((brand) => brand.checked)
                  .map((brand) => brand.id),
              });
            }}
          />
          <input
            type="submit"
            value="Сбросить"
            onClick={() => {
              clearFilters(priceMin, priceMax, setBrands, appData.setCurrentPage);
              applyFilters({ getProducts, appData });
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default SortBarLeft;
