import styles from "./CartPageSummary.module.css";
import { handleCheckout } from "./apiCartPageSummary";

function CartPageSummary({ cartProductsObject, setCartProductsObject, setSelectedCartProductsIds }) {
    console.log(cartProductsObject.total_quantity, cartProductsObject.total_price);

    return (
        <div className={styles.cart_page_summary_section_wrapper}>
            <h2 className={styles.cart_page_summary_section_header}>Условия заказа</h2>
            <div>
                <div className={styles.cart_page_summary_section_row}>
                    <h3>Товара:</h3>
                    <h3>{cartProductsObject.total_quantity}</h3>
                </div>

                <div className={styles.cart_page_summary_section_row}>
                    <h3>Итого:</h3>
                    <h3>{cartProductsObject.total_price} &#8381;</h3>
                </div>

                <div className={styles.cart_page_summary_section_button_wrapper}>
                    <button
                        className={styles.cart_page_summary_section_button}
                        onClick={() => handleCheckout(cartProductsObject.cart_products, setCartProductsObject, setSelectedCartProductsIds)}
                    > 
                        Оформить заказ
                    </button>
                </div>
            </div>
        </div>
    );
};

export default CartPageSummary;