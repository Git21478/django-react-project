export const handleOrderingChange = (orderingType, orderingDirection, setOrdering) => {
    let orderingQuery = "";
    if (orderingDirection === "descending") {
        orderingQuery = "-";
    };
    orderingQuery = `${orderingQuery}${orderingType}`;
    setOrdering(orderingQuery);
};