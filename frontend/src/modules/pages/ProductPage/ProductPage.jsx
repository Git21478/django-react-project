import styles from "./ProductPage.module.css";
import { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import { getProduct, getReviews } from "./apiProductPage";
import ReviewCreation from "./ReviewCreation/ReviewCreation";
import Review from "./Review/Review";
import Product from "../../components/Product/Product";
import { AppContext } from "../../AppProvider/AppProvider";
import { frontendBaseURL } from "../../../constants";
import PageTemplate from "../../PageTemplate/PageTemplate";
import ReviewSortBar from "./ReviewSortBar/ReviewSortBar";

function ProductPage() {
    const [pageTitle, setPageTitle] = useState("Товар");
    document.title = `${pageTitle} | Магазин`;
    const appData = useContext(AppContext);
    const productId = useParams().product_id;
    const [category, setCategory] = useState("");
    const [product, setProduct] = useState("");
    const [reviews, setReviews] = useState([]);

    useEffect(() => {
        getProduct(productId, setProduct);
    }, []);

    useEffect(() => {
        getReviews(productId, appData.reviewsOrdering, setReviews);
    }, [appData.reviewsOrdering]);

    useEffect(() => {
        (appData.categories && product.category) && setCategory(appData.categories.find(category1 => category1.id === product.category));
    }, [appData.categories, product]);

    useEffect(() => {
        product && setPageTitle(product.name);
    }, [product]);

    return (
        <PageTemplate>
            <div className={styles.product_page_wrapper}>
                <div>
                    <a href={`${frontendBaseURL}/catalog/${category.slug}`}>{category.name}</a> {">"} {pageTitle}
                </div>

                <div>
                    {product && <Product product={product}/>}
                </div>

                <div>
                    <div className={styles.product_page_reviews_section}>
                        <div>
                            <ReviewCreation product_id={productId} reviewsOrdering={appData.reviewsOrdering} setReviews={setReviews}/>
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