export const handleCheckboxCartProduct = (e, selectedCartProductIds, setSelectedCartProductIds) => {
    let value = parseInt(e.target.value);

    if (e.target.checked) {
        setSelectedCartProductIds([...selectedCartProductIds, value]);
    } else {
        setSelectedCartProductIds(prevData => {
            return prevData.filter(id => {
                return id !== value;
            });
        });
    };
};