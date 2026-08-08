import styles from "./CartProduct.module.css";
import { useInput } from "../../../../hooks/useInput.js";
import {
  changeCartProductQuantity,
  addFavorite,
  deleteFavorite,
  deleteCartProduct,
} from "./apiCartProduct.js";
import favorites_0_icon from "../../../../assets/icons/favorites_0.png";
import favorites_1_icon from "../../../../assets/icons/favorites_1.png";
import delete_icon from "../../../../assets/icons/delete.png";
import { handleCheckboxCartProduct } from "./utilsCartProduct.js";
import { getCart } from "../apiCartPage.js";
import { Link } from "react-router-dom";

function CartProduct({
  cartProduct,
  setCart,
  selectedCartProductIds,
  setSelectedCartProductIds,
}) {
  const quantity = useInput(cartProduct.quantity);

  return (
    <div className={styles.cart_product_container}>
      <div className={styles.cart_product_image}>
        <img src={cartProduct.product.image} alt="Cart product image" />
        <input
          className={styles.cart_product_checkbox}
          type="checkbox"
          value={cartProduct.id}
          checked={selectedCartProductIds.includes(cartProduct.id)}
          onChange={(e) =>
            handleCheckboxCartProduct(
              e,
              selectedCartProductIds,
              setSelectedCartProductIds,
            )
          }
        />
      </div>

      <div className={styles.cart_product_info}>
        <div className={styles.cart_product_top}>
          <h2 className={styles.cart_product_title}>
            <Link to={`/products/${cartProduct.product.id}`}>
              {cartProduct.product.name}
            </Link>
          </h2>
          <p className={styles.cart_product_description}>
            {cartProduct.product.description}
          </p>
        </div>

        <div className={styles.cart_product_bottom}>
          <div className={styles.cart_product_bottom_price}>
            <h3>{cartProduct.product.price} &#8381; &nbsp;</h3>

            <h3>
              <button
                onClick={() => {
                  changeCartProductQuantity(
                    cartProduct.product.id,
                    quantity.value - 1,
                    setCart,
                  );
                }}
              >
                -
              </button>

              <input {...quantity.input} type="text" />

              <button
                onClick={() => {
                  changeCartProductQuantity(
                    cartProduct.product.id,
                    quantity.value + 1,
                    setCart,
                  );
                }}
              >
                +
              </button>
            </h3>

            <h3 className={styles.cart_product_price}>
              &nbsp; {cartProduct.product.price * quantity.value} &#8381;
            </h3>
          </div>

          <div>
            {!cartProduct.product.is_favorite ? (
              <img
                className={styles.cart_product_icon}
                src={favorites_0_icon}
                alt="Favorites icon"
                onClick={() => addFavorite(cartProduct.product.id, setCart)}
              />
            ) : (
              <img
                className={styles.cart_product_icon}
                src={favorites_1_icon}
                alt="Favorites icon"
                onClick={() =>
                  deleteFavorite(cartProduct.product.favorite_id, setCart)
                }
              />
            )}

            <img
              className={styles.cart_product_icon}
              src={delete_icon}
              alt="Delete icon"
              onClick={() => deleteCartProduct(cartProduct.product.id, setCart)}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default CartProduct;
