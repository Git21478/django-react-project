import styles from "./SortBarLeft.module.css";
import { getCurrentCategoryBrands } from "./apiSortBarLeft";
import { useContext, useEffect, useState } from "react";
import { useInput } from "../../../hooks/useInput";
import { AppContext } from "../../AppProvider/AppProvider";
import { getFilteredProducts } from "../../pages/HomePage/apiHomePage";
import { clearFilters } from "./utilsSortBarLeft";

function SortBarLeft() {
    const appData = useContext(AppContext);
    const priceMin = useInput("");
    const priceMax = useInput("");
    const [brands, setBrands] = useState();

    const handleCheckboxChange = (id) => {
        setBrands(brands.map(brand => {
            return brand.id === id ? {...brand, checked: !brand.checked} : brand;
        }));
    };

    useEffect(() => {
        getCurrentCategoryBrands(appData.currentCategory, setBrands);
    }, [appData.currentCategory.brands]);

    return (
        <div className={styles.sort_bar_left_wrapper}>
            <h1 className={styles.product_sort_menu_header}>{appData.currentCategory.name}</h1>

            <div>
                <div className={styles.filter_element}>
                    <h2>Цена</h2>
                    <input type="text" placeholder="от" {...priceMin.input}/>
                    <input type="text" placeholder="до" {...priceMax.input}/>
                </div>

                <div className={styles.filter_element}>
                    <h2>Производитель</h2>
                    <div>
                        {brands && brands !== "" && brands.map((brand) => {
                            return (
                                <div key={brand.id}>
                                    <label>
                                        <input type="checkbox" checked={brand.checked} onChange={() => handleCheckboxChange(brand.id)}/>
                                        {brand.name}
                                    </label>
                                </div>
                            )
                        })}
                    </div>
                </div>

                <div className={styles.filter_element}>
                    <input type="submit" value="Применить" onClick={() => getFilteredProducts(appData, priceMin.value, priceMax.value, brands)}/>
                    <input type="submit" value="Сбросить" onClick={() => clearFilters(priceMin, priceMax)}/>
                </div>
            </div>
        </div>
    );
};

export default SortBarLeft;