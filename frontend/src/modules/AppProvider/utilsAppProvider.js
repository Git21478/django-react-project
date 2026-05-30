export const createPages = (productCount, pageSize, setPages) => {
    if (productCount !== 0) {
        const pageCount = Math.ceil(productCount / pageSize);
        let pages_temp = [];
        for (let i = 1; i <= pageCount; i++) {
            pages_temp.push(i);
        }
        setPages(pages_temp);
    };
};