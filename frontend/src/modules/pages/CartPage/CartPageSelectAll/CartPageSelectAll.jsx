import styles from "./CartPageSelectAll.module.css";
import { deleteMultipleCartProducts } from "../apiCartPage";
import { handleCheckboxAllCartProducts } from "../utilsCartPage";

function CartPageSelectAll({ cart, setCart, selectedCartProductIds, setSelectedCartProductIds }) {
    return (
        <div className={styles.cart_page_select_section}>
            <div className={styles.cart_page_select_all}>
                <input
                    type="checkbox"
                    id="checkboxAll"
                    checked={selectedCartProductIds.length === cart.cart_products.length && selectedCartProductIds.length !== 0}
                    onChange={() => handleCheckboxAllCartProducts(cart.cart_products, selectedCartProductIds, setSelectedCartProductIds)}
                />
                <label htmlFor="checkboxAll"><h2>Выбрать все</h2></label>
            </div>
            
            {selectedCartProductIds.length !== 0 && 
                <h2 onClick={() => deleteMultipleCartProducts(selectedCartProductIds, setSelectedCartProductIds, setCart)}>Удалить выбранные товары</h2>
            }
        </div>
    );
};

export default CartPageSelectAll;