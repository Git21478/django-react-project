export const handleOrderingChange = (orderingType, orderingDirection, setReviewsOrdering) => {
    let orderingQuery = "";
    if (orderingDirection === "descending") {
        orderingQuery = "-";
    }
    orderingQuery = `${orderingQuery}${orderingType}`;
    setReviewsOrdering(orderingQuery);
};