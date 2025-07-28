import styles from "./HomePage.module.css";
import SortBarCenter from "../../components/SortBarCenter/SortBarCenter";
import Product from "../../components/Product/Product";
import Pagination from "../../components/Pagination/Pagination";
import PageTemplate from "../../PageTemplate/PageTemplate";
import { useContext } from "react";
import { AppContext } from "../../AppProvider/AppProvider";

function HomePage() {
    document.title = "Главная страница | Магазин";
    const appData = useContext(AppContext);

    return (
        <PageTemplate>
            <div className={styles.home_page_products_wrapper}>
                <SortBarCenter
                    setProductsOrdering={appData.setProductsOrdering}
                />

                <div>
                    {appData.products.map(product => (
                        <Product
                            product={product}
                            setProducts={appData.setProducts}
                            key={product.id}
                        />
                    ))}
                </div>
                
                <Pagination
                    currentPage={appData.currentPage}
                    setCurrentPage={appData.setCurrentPage}
                    pages={appData.pages}
                />
            </div>
        </PageTemplate>
    );
};

export default HomePage;