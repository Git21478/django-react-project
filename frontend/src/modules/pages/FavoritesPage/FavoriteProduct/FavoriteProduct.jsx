import styles from "./FavoriteProduct.module.css";
import favorites_1_icon from "../../../../assets/icons/favorites_1.png";
import { handleCheckboxFavoriteProduct, pluralize } from "./utilsFavoriteProduct.js";
import { addCartProduct, deleteFavoriteProduct } from "./apiFavoriteProduct.js";

function FavoriteProduct({ favoriteProduct, setFavoriteProducts, selectedFavoriteProductsIds, setSelectedFavoriteProductsIds }) {
    const pluralizedReviews = favoriteProduct && pluralize(["отзыв", "отзыва", "отзывов"], favoriteProduct.product.review_amount);

    return (
        <div className={styles.favorite_product_container}>
            <div className={styles.favorite_product_image}>
                <img src={favoriteProduct.product.image} alt="Product image"/>
                <input
                    className={styles.favorite_product_checkbox}
                    type="checkbox"
                    value={favoriteProduct.id}
                    checked={selectedFavoriteProductsIds.includes(favoriteProduct.id)}
                    onChange={(e) => handleCheckboxFavoriteProduct(e, selectedFavoriteProductsIds, setSelectedFavoriteProductsIds)}
                />
            </div>

            <div className={styles.favorite_product_info}>
                <div className={styles.favorite_product_title_date}>
                    <h2 className={styles.favorite_product_title}><a href={`/products/${favoriteProduct.product.id}`}>{favoriteProduct.product.name}</a></h2>
                    <h2>{favoriteProduct.product.price} &#8381;</h2>
                </div>

                <div className={styles.favorite_product_bottom}>
                    <h3>* {favoriteProduct.product.rating} | {favoriteProduct.product.review_amount} {pluralizedReviews}</h3>
                    <div>
                        <img className={styles.favorite_product_icon} src={favorites_1_icon} alt="Favorites" onClick={() => deleteFavoriteProduct(favoriteProduct.id, setFavoriteProducts)}/>

                        {!favoriteProduct.product.is_cart_product
                            ? <button className={styles.favorite_product_add_to_cart_button} onClick={() => addCartProduct(favoriteProduct.product.id, setFavoriteProducts)}>Купить</button>
                            : <button className={styles.favorite_product_cart_page_link_button}><a href="/cart">В корзине</a></button>
                        }
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FavoriteProduct;