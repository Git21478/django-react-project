import styles from "./Product.module.css";
import star_icon from "../../../assets/icons/star.png";
import favorites_0_icon from "../../../assets/icons/favorites_0.png";
import favorites_1_icon from "../../../assets/icons/favorites_1.png";
import { pluralize } from "./utilsProduct.js";
import { addCartProduct, addFavoriteProduct, deleteFavoriteProduct } from "./apiProduct.js";

function Product({ product, setProducts }) {
    const pluralizedReviews = product && pluralize(["отзыв", "отзыва", "отзывов"], product.review_amount);

    return (
        <div className={styles.product_container}>
            <div className={styles.product_image}>
                <img src={product.image} alt="Product image"/>
            </div>

            <div className={styles.product_info}>
                <div className={styles.product_title_date}>
                    <h2 className={styles.product_title}><a href={`/products/${product.id}`}>{product.name}</a></h2>
                    <h2>{product.price} &#8381;</h2>
                </div>

                <div className={styles.product_bottom}>
                    <h3 className={styles.product_bottom_left_section}>
                        {product.review_amount != 0
                            ? <span><img className={styles.star_icon} src={star_icon} alt="Star icon"/> {product.rating} | {product.review_amount} {pluralizedReviews}</span>
                            : <span>Нет отзывов</span>
                        } 
                    </h3>
                    <div>
                        {!product.is_favorite_product
                            ? <img className={styles.product_icon} src={favorites_0_icon} alt="Favorites" onClick={() => addFavoriteProduct(product.id, setProducts)}/>
                            : <img className={styles.product_icon} src={favorites_1_icon} alt="Favorites" onClick={() => deleteFavoriteProduct(product.favorite_product_id, setProducts)}/>
                        }

                        {!product.is_cart_product
                            ? <button className={styles.product_add_to_cart_button} onClick={() => addCartProduct(product.id, setProducts)}>Купить</button>
                            : <button className={styles.product_cart_page_link_button}><a href="/cart">В корзине</a></button>
                        }
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Product;