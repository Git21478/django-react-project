import styles from "./ProductPage.module.css";
import { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import { getProductPageProduct, getReviews } from "./apiProductPage";
import ReviewCreation from "./ReviewCreation/ReviewCreation";
import Review from "./Review/Review";
import { AppContext } from "../../AppProvider/AppProvider";
import PageTemplate from "../../PageTemplate/PageTemplate";
import ReviewSortBar from "./ReviewSortBar/ReviewSortBar";
import ProductPageProduct from "./ProductPageProduct/ProductPageProduct";

function ProductPage() {
    const [pageTitle, setPageTitle] = useState("Товар");
    document.title = `${pageTitle} | Магазин`;
    const appData = useContext(AppContext);
    const productPageProductId = useParams().product_id;
    const [category, setCategory] = useState("");
    const [productPageProduct, setProductPageProduct] = useState("");
    const [reviews, setReviews] = useState([]);

    useEffect(() => {
        getProductPageProduct(productPageProductId, setProductPageProduct);
    }, []);

    useEffect(() => {
        getReviews(productPageProductId, appData.reviewsOrdering, setReviews);
    }, [appData.reviewsOrdering]);

    useEffect(() => {
        (appData.categories && productPageProduct.category) && setCategory(appData.categories.find(category1 => category1.id === productPageProduct.category));
    }, [appData.categories, productPageProduct]);

    useEffect(() => {
        productPageProduct && setPageTitle(productPageProduct.name);
    }, [productPageProduct]);

    return (
        <PageTemplate>
            <div className={styles.product_page_wrapper}>
                <div>
                    <a href={`/catalog/${category.slug}`}>{category.name}</a> {">"} {pageTitle}
                </div>

                <div>
                    {productPageProduct && <ProductPageProduct productPageProduct={productPageProduct} setProductPageProduct={setProductPageProduct}/>}
                </div>

                <div>
                    <div className={styles.product_page_reviews_section}>
                        <div>
                            <ReviewCreation product_id={productPageProductId} reviewsOrdering={appData.reviewsOrdering} setReviews={setReviews}/>
                        </div>

                        <div className={styles.product_page_sorting_and_reviews_section}>
                            <div>
                                <ReviewSortBar setReviewsOrdering={appData.setReviewsOrdering}/>
                            </div>

                            <div>
                                {reviews && reviews.map(review => (
                                    <Review reviewObject={review} reviewsOrdering={appData.reviewsOrdering} setReviews={setReviews} key={review.id}/>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </PageTemplate>
    );
};

export default ProductPage;