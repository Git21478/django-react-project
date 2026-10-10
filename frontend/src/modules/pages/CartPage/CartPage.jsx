import styles from "./CartPage.module.css";
import { useContext, useEffect, useState } from "react";
import { getCart } from "./apiCartPage";
import PageTemplate from "../../PageTemplate/PageTemplate";
import Cart from "./CartProduct/CartProduct";
import { AppContext } from "../../AppProvider/AppProvider";
import CartPageSelectAll from "./CartPageSelectAll/CartPageSelectAll";
import CartProduct from "./CartProduct/CartProduct";
import CartPageSummary from "./CartPageSummary/CartPageSummary";

function CartPage() {
  document.title = "Корзина | Магазин";
  const { cart, setCart } = useContext(AppContext);
  const [selectedCartProductIds, setSelectedCartProductIds] = useState([]);

  useEffect(() => {
    getCart(setCart);
  }, []);

  return (
    <PageTemplate>
      <div className={styles.cart_page_wrapper}>
        <h1 className={styles.cart_page_header}>Корзина</h1>

        {cart && (
          <CartPageSelectAll
            cart={cart}
            setCart={setCart}
            selectedCartProductIds={selectedCartProductIds}
            setSelectedCartProductIds={setSelectedCartProductIds}
          />
        )}

        <div className={styles.cart_page_main_section}>
          <div className={styles.cart_page_products_section}>
            {cart.cart_products &&
              cart.cart_products.map((cartProduct) => (
                <CartProduct
                  cartProduct={cartProduct}
                  setCart={setCart}
                  selectedCartProductIds={selectedCartProductIds}
                  setSelectedCartProductIds={setSelectedCartProductIds}
                  key={cartProduct.id}
                />
              ))}
          </div>

          <div className={styles.cart_page_summary_section}>
            <CartPageSummary
              cart={cart}
              setCart={setCart}
              setSelectedCartProductIds={setSelectedCartProductIds}
            />
          </div>
        </div>
      </div>
    </PageTemplate>
  );
}

export default CartPage;
