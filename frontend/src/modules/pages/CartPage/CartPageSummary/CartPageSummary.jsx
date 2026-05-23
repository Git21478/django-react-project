import styles from "./CartPageSummary.module.css";
import { handleCheckout } from "./apiCartPageSummary";

function CartPageSummary({ cart, setCart, setSelectedCartProductIds }) {
    return (
        <div className={styles.cart_page_summary_section_wrapper}>
            <h2 className={styles.cart_page_summary_section_header}>Условия заказа</h2>
            <div>
                <div className={styles.cart_page_summary_section_row}>
                    <h3>Товара:</h3>
                    <h3>{cart.total_quantity}</h3>
                </div>

                <div className={styles.cart_page_summary_section_row}>
                    <h3>Итого:</h3>
                    <h3>{cart.total_price} &#8381;</h3>
                </div>

                <div className={styles.cart_page_summary_section_button_wrapper}>
                    <button
                        className={styles.cart_page_summary_section_button}
                        onClick={() => handleCheckout(cart.cart_products, setCart)}
                    > 
                        Оформить заказ
                    </button>
                </div>
            </div>
        </div>
    );
};

export default CartPageSummary;