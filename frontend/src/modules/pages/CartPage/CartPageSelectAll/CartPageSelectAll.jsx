import styles from "./CartPageSelectAll.module.css";
import { deleteMultipleCartProducts } from "../apiCartPage";
import { handleCheckboxAllCartProducts } from "../utilsCartPage";

function CartPageSelectAll({ cartProductsObject, setCartProductsObject, selectedCartProductsIds, setSelectedCartProductsIds }) {
    console.log(cartProductsObject);
    console.log(cartProductsObject);
    console.log(cartProductsObject);
    
    return (
        <div className={styles.cart_page_select_section}>
            <div className={styles.cart_page_select_all}>
                <input
                    type="checkbox"
                    id="checkboxAll"
                    checked={selectedCartProductsIds.length === cartProductsObject.cart_products.length && selectedCartProductsIds.length !== 0}
                    onChange={() => handleCheckboxAllCartProducts(cartProductsObject.cart_products, selectedCartProductsIds, setSelectedCartProductsIds)}
                />
                <label htmlFor="checkboxAll"><h2>Выбрать все</h2></label>
            </div>
            
            {selectedCartProductsIds.length !== 0 && 
                <h2 onClick={() => deleteMultipleCartProducts(selectedCartProductsIds, setCartProductsObject)}>Удалить выбранные товары</h2>
            }
        </div>
    );
};

export default CartPageSelectAll;