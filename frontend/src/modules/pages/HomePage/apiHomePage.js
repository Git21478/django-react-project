import api from "../../../api";

export const getProducts = (setProducts, setProductsAmount, currentPage, pageSize, ordering, search="") => {
    api
        .get(`/api/products/?pageSize=${pageSize}&page=${currentPage}&ordering=${ordering}&search=${search}`)
        .then((res) => {
            setProducts(res.data.results);
            setProductsAmount(res.data.count);
            console.log(res.data.results);
        })
        .catch((err) => console.log(err));
};

export const getCategoryProducts = (setProducts, setProductsAmount, currentPage, pageSize, ordering, search="", categorySlug="") => {
    api
        .get(`/api/catalog/${categorySlug}/products/?pageSize=${pageSize}&page=${currentPage}&ordering=${ordering}&search=${search}`)
        .then((res) => {
            setProducts(res.data.results);
            setProductsAmount(res.data.count);
            console.log(res.data.results);
        })
        .catch((err) => console.log(err));
};

export const getFilteredProducts = (appData, priceMin, priceMax, selectedBrands) => {
    let url = `/api/catalog/${appData.currentCategory.id}/products/?pageSize=${appData.pageSize}&page=${appData.currentPage}&ordering=${appData.ordering}&search=${appData.search}`;
    if (priceMin !== "") url += `&priceMin=${priceMin}`;
    if (priceMax !== "") url += `&priceMax=${priceMax}`;

    console.log(priceMin, priceMax);
    console.log(selectedBrands.value);
    api
        .get(url)
        .then((res) => {
            appData.setIsGetFilteredProducts(true);
            appData.setProducts(res.data.results);
            appData.setProductsAmount(res.data.count);
            console.log(res.data.results);
        })
        .catch((err) => console.log(err));
};