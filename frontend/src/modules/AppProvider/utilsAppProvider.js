export const createPages = (productsAmount, pageSize, setPages) => {
    if (productsAmount !== 0) {
        const pageAmount = Math.ceil(productsAmount / pageSize);
        let pages_temp = [];
        for (let i = 1; i <= pageAmount; i++) {
            pages_temp.push(i);
        }
        setPages(pages_temp);
    };
};