import api from "../../../../api";

export const handleCheckout = (cartProducts, setCart) => {
  api
    .delete("api/cart/clear/")
    .then((res) => {
      console.log(res);
      setCart(res.data);
      alert("Заказ оформлен");
    })
    .catch((error) => {
      console.log(error);
    });
};
