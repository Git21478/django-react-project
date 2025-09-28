import styles from "./ProductPageProduct.module.css";
import star_icon from "../../../../assets/icons/star.png";
import favorites_0_icon from "../../../../assets/icons/favorites_0.png";
import favorites_1_icon from "../../../../assets/icons/favorites_1.png";
import { pluralize } from "./utilsProductPageProduct.js";
import { addCartProduct, addFavoriteProduct, deleteFavoriteProduct } from "./apiProductPageProduct.js";

function ProductPageProduct({ productPageProduct, setProductPageProduct }) {
    const pluralizedReviews = productPageProduct && pluralize(["отзыв", "отзыва", "отзывов"], productPageProduct.review_amount);

    return (
        <div className={styles.product_container}>
            <div className={styles.product_top}>
                <div className={styles.product_image}>
                    <img src={productPageProduct.image} alt="Product image"/>
                </div>

                <div className={styles.product_info}>
                    <div className={styles.product_title_date}>
                        <div className={styles.product_title}>
                            <h2 className={styles.product_title_name}><a href={`/products/${productPageProduct.id}`}>{productPageProduct.name}</a></h2>
                            <h2 className={styles.product_title_price}>{productPageProduct.price} &#8381;</h2>
                        </div>
                        <p className={styles.product_description}>{productPageProduct.description}</p>
                    </div>
                </div>
            </div>

            <div className={styles.product_bottom}>
                <h3 className={styles.product_bottom_left_section}>
                    {productPageProduct.review_amount != 0
                        ? <span><img className={styles.star_icon} src={star_icon} alt="Star icon"/> {productPageProduct.rating} | {productPageProduct.review_amount} {pluralizedReviews}</span>
                        : <span>Нет отзывов</span>
                    } 
                </h3>
                <div>
                    {!productPageProduct.is_favorite_product
                        ? <img className={styles.product_icon} src={favorites_0_icon} alt="Favorites" onClick={() => addFavoriteProduct(productPageProduct.id, setProductPageProduct)}/>
                        : <img className={styles.product_icon} src={favorites_1_icon} alt="Favorites" onClick={() => deleteFavoriteProduct(productPageProduct.favorite_product_id, setProductPageProduct)}/>
                    }

                    {!productPageProduct.is_cart_product
                        ? <button className={styles.product_add_to_cart_button} onClick={() => addCartProduct(productPageProduct.id, setProductPageProduct)}>Купить</button>
                        : <button className={styles.product_cart_page_link_button}><a href="/cart">В корзине</a></button>
                    }
                </div>
            </div>
        </div>
    );
};

export default ProductPageProduct;