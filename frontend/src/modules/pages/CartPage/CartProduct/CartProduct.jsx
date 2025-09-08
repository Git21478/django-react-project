import styles from "./CartProduct.module.css";
import { useInput } from "../../../../hooks/useInput.js";
import { changeCartProductQuantity, addFavoriteProduct, deleteFavoriteProduct, deleteCartProduct } from "./apiCartProduct.js";
import favorites_0_icon from "../../../../assets/icons/favorites_0.png";
import favorites_1_icon from "../../../../assets/icons/favorites_1.png";
import delete_icon from "../../../../assets/icons/delete.png";
import { handleCheckboxCartProduct } from "./utilsCartProduct.js";
import { getCartProducts } from "../apiCartPage.js";

function CartProduct({ cartProduct, setCartProductsObject, selectedCartProductsIds, setSelectedCartProductsIds }) {
    const quantity = useInput(cartProduct.quantity);
    console.log(cartProduct);

    return (
        <div className={styles.cart_product_container}>
            <div className={styles.cart_product_image}>
                <img src={cartProduct.product.image} alt="Cart product image"/>
                <input
                    className={styles.cart_product_checkbox}
                    type="checkbox"
                    value={cartProduct.id}
                    checked={selectedCartProductsIds.includes(cartProduct.id)}
                    onChange={(e) => handleCheckboxCartProduct(e, selectedCartProductsIds, setSelectedCartProductsIds)}
                />
            </div>

            <div className={styles.cart_product_info}>
                <div className={styles.cart_product_title_date}>
                    <h2 className={styles.cart_product_title}><a href={`/products/${cartProduct.product.id}`}>{cartProduct.product.name}</a></h2>
                </div>

                <div className={styles.cart_product_bottom}>
                    <div className={styles.cart_product_bottom_price}>
                        <h3>{cartProduct.product.price} &#8381;</h3>

                        <h3>
                            <button onClick={() => {
                                quantity.setValue(prevState => prevState - 1);
                                changeCartProductQuantity(cartProduct.id, quantity.value - 1, setCartProductsObject);
                            }}>
                                -
                            </button>

                            <input
                                {...quantity.input}
                                type="text"
                            />

                            <button onClick={() => {
                                quantity.setValue(prevState => prevState + 1);
                                changeCartProductQuantity(cartProduct.id, quantity.value + 1, setCartProductsObject);
                            }}>
                                +
                            </button>
                        </h3>
                    
                        <h3 className={styles.cart_product_price}>
                            {cartProduct.product.price * quantity.value} &#8381;
                        </h3>
                    </div>

                    <div>
                        {!cartProduct.product.is_favorite_product
                            ? <img className={styles.cart_product_icon} src={favorites_0_icon} alt="Favorites icon" onClick={() => addFavoriteProduct(cartProduct.product.id, setCartProductsObject)}/>
                            : <img className={styles.cart_product_icon} src={favorites_1_icon} alt="Favorites icon" onClick={() => deleteFavoriteProduct(cartProduct.product.favorite_product_id, setCartProductsObject)}/>
                        }

                        <img className={styles.cart_product_icon} src={delete_icon} alt="Delete icon" onClick={() => deleteCartProduct(cartProduct.id, getCartProducts, setCartProductsObject)}/>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CartProduct;