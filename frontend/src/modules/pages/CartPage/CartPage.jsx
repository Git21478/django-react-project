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
    const appData = useContext(AppContext);
    const [selectedCartProductIds, setSelectedCartProductIds] = useState([]);

    useEffect(() => {
        getCart(appData.setCart);
        console.log(appData);
    }, []);

    return (
        <PageTemplate>
            <div className={styles.cart_page_wrapper}>
                <h1 className={styles.cart_page_header}>Корзина</h1>

                {appData.cart &&
                    <CartPageSelectAll
                        cart={appData.cart}
                        setCart={appData.setCart}
                        selectedCartProductIds={selectedCartProductIds}
                        setSelectedCartProductIds={setSelectedCartProductIds}
                    />
                }

                <div className={styles.cart_page_main_section}>
                    <div className={styles.cart_page_products_section}>
                        {appData.cart.cart_products && appData.cart.cart_products.map(cartProduct => (
                            <CartProduct
                                cartProduct={cartProduct}
                                setCart={appData.setCart}
                                selectedCartProductIds={selectedCartProductIds}
                                setSelectedCartProductIds={setSelectedCartProductIds}
                                key={cartProduct.id}
                            />
                        ))}
                    </div>

                    <div className={styles.cart_page_summary_section}>
                        <CartPageSummary
                            cart={appData.cart}
                            setCart={appData.setCart}
                            setSelectedCartProductIds={setSelectedCartProductIds}
                        />
                    </div>
                </div>
            </div>
        </PageTemplate>
    );
};

export default CartPage;