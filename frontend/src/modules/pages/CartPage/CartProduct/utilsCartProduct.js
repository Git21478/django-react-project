export const handleCheckboxCartProduct = (e, selectedCartProductsIds, setSelectedCartProductsIds) => {
    let value = parseInt(e.target.value);

    if (e.target.checked) {
        setSelectedCartProductsIds([...selectedCartProductsIds, value]);
    } else {
        setSelectedCartProductsIds(prevData => {
            return prevData.filter(id => {
                return id !== value;
            });
        });
    };
};