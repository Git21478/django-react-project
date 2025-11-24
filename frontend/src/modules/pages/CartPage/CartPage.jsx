import styles from "./CartPage.module.css";
import { useContext, useEffect, useState } from "react";
import { getCartProducts } from "./apiCartPage";
import PageTemplate from "../../PageTemplate/PageTemplate";
import CartProduct from "./CartProduct/CartProduct";
import { AppContext } from "../../AppProvider/AppProvider";
import CartPageSelectAll from "./CartPageSelectAll/CartPageSelectAll";
import CartPageSummary from "./CartPageSummary/CartPageSummary";

function CartPage() {
    document.title = "Корзина | Магазин";
    const appData = useContext(AppContext);
    const [selectedCartProductsIds, setSelectedCartProductsIds] = useState([]);

    useEffect(() => {
        getCartProducts(appData.setCartProductsObject);
    }, []);

    return (
        <PageTemplate>
            <div className={styles.cart_page_wrapper}>
                <h1 className={styles.cart_page_header}>Корзина</h1>

                {appData.cartProductsObject &&
                    <CartPageSelectAll
                        cartProductsObject={appData.cartProductsObject}
                        setCartProductsObject={appData.setCartProductsObject}
                        selectedCartProductsIds={selectedCartProductsIds}
                        setSelectedCartProductsIds={setSelectedCartProductsIds}
                    />
                }

                <div className={styles.cart_page_main_section}>
                    <div className={styles.cart_page_products_section}>
                        {appData.cartProductsObject.cart_products && appData.cartProductsObject.cart_products.map(cartProduct => (
                            <CartProduct
                                cartProduct={cartProduct}
                                setCartProductsObject={appData.setCartProductsObject}
                                selectedCartProductsIds={selectedCartProductsIds}
                                setSelectedCartProductsIds={setSelectedCartProductsIds}
                                key={cartProduct.id}
                            />
                        ))}
                    </div>

                    <div className={styles.cart_page_summary_section}>
                        <CartPageSummary
                            cartProductsObject={appData.cartProductsObject}
                            setCartProductsObject={appData.setCartProductsObject}
                            setSelectedCartProductsIds={setSelectedCartProductsIds}
                        />
                    </div>
                </div>
            </div>
        </PageTemplate>
    );
};

export default CartPage;