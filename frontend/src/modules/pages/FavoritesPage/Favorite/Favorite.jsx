import styles from "./Favorite.module.css";
import star_icon from "../../../../assets/icons/star.png";
import favorites_1_icon from "../../../../assets/icons/favorites_1.png";
import { handleCheckboxFavorite, pluralize } from "./utilsFavorite.js";
import { addCartProduct, deleteFavorite } from "./apiFavorite.js";
import { Link } from "react-router-dom";

function Favorite({
  favorite,
  setFavorites,
  selectedFavoritesIds,
  setSelectedFavoritesIds,
}) {
  const pluralizedReviews =
    favorite &&
    pluralize(["отзыв", "отзыва", "отзывов"], favorite.product.review_count);

  return (
    <div className={styles.favorite_container}>
      <div className={styles.favorite_image}>
        <img src={favorite.product.image} alt="Product image" />
        <input
          className={styles.favorite_checkbox}
          type="checkbox"
          value={favorite.id}
          checked={selectedFavoritesIds.includes(favorite.id)}
          onChange={(e) =>
            handleCheckboxFavorite(
              e,
              selectedFavoritesIds,
              setSelectedFavoritesIds,
            )
          }
        />
      </div>

      <div className={styles.favorite_info}>
        <div>
          <div className={styles.favorite_title}>
            <h2 className={styles.favorite_title}>
              <Link to={`/products/${favorite.product.id}`}>
                {favorite.product.name}
              </Link>
            </h2>
            <h2>{favorite.product.price} &#8381;</h2>
          </div>
          <p className={styles.favorite_description}>
            {favorite.product.description}
          </p>
        </div>

        <div className={styles.favorite_bottom}>
          <h3>
            <img className={styles.star_icon} src={star_icon} alt="Star icon" />{" "}
            {favorite.product.rating} | {favorite.product.review_count}{" "}
            {pluralizedReviews}
          </h3>
          <div>
            <img
              className={styles.favorite_icon}
              src={favorites_1_icon}
              alt="Favorites"
              onClick={() => deleteFavorite(favorite.id, setFavorites)}
            />

            {!favorite.product.is_cart_product ? (
              <button
                className={styles.favorite_add_to_cart_button}
                onClick={() =>
                  addCartProduct(favorite.product.id, setFavorites)
                }
              >
                Купить
              </button>
            ) : (
              <button className={styles.favorite_cart_page_link_button}>
                <Link to="/cart">В корзине</Link>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Favorite;
