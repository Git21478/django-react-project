import api from "../../../../api";

export const handleCheckout = (cartProducts, setCart) => {
  api
    .delete("cart/clear/")
    .then((res) => {
      setCart(res.data);
      alert("Заказ оформлен");
    })
    .catch((error) => {
      console.error(error);
    });
};
