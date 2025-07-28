import styles from "./CategoryPage.module.css";
import SortBarCenter from "../../components/SortBarCenter/SortBarCenter";
import Product from "../../components/Product/Product";
import Pagination from "../../components/Pagination/Pagination";
import SortBarLeft from "../../components/SortBarLeft/SortBarLeft";
import { useContext, useEffect } from "react";
import { useParams } from "react-router-dom";
import { AppContext } from "../../AppProvider/AppProvider";
import PageTemplate from "../../PageTemplate/PageTemplate";

function CategoryPage() {
    const appData = useContext(AppContext);
    const categorySlug = useParams().category_slug;
    document.title = `${appData.currentCategory.name} | Магазин`;

    useEffect(() => {
        appData.setCurrentCategorySlug(categorySlug);
    }, []);

    return (
        <PageTemplate>
            <div className={styles.category_page_wrapper}>
                <div className={styles.sort_bar_left}>
                    <SortBarLeft/>
                </div>

                <div className={styles.products_and_pagination}>
                    <div>
                        <SortBarCenter
                            setProductsOrdering={appData.setProductsOrdering}
                        />
                    </div>

                    <div>
                        {appData.products.map(product => (
                            <Product
                                product={product}
                                setProducts={appData.setProducts}
                                key={product.id}
                            />
                        ))}

                        <Pagination
                            currentPage={appData.currentPage}
                            setCurrentPage={appData.setCurrentPage}
                            pages={appData.pages}
                        />
                    </div>
                </div>
            </div>
        </PageTemplate>
    );
};

export default CategoryPage;