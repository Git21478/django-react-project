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

export const getFilteredProducts = (appData, priceMin, priceMax, brands) => {
    const selectedBrandsIds = brands
        .filter(brand => brand.checked === true)
        .map(brand => brand.id);

    console.log(appData);
    let url = `/api/catalog/${appData.currentCategory.id}/products/?pageSize=${appData.pageSize}&page=${appData.currentPage}&ordering=${appData.ordering}&search=${appData.search}`;
    if (priceMin !== "") url += `&price_min=${priceMin}`;
    if (priceMax !== "") url += `&price_max=${priceMax}`;
    if (selectedBrandsIds !== "") url += `&selected_brands_ids=${selectedBrandsIds}`

    console.log(priceMin, priceMax);
    console.log(selectedBrandsIds);

    api
        .get(url)
        .then((res) => {
            console.log(res.data.results);
            appData.setIsGetFilteredProducts(true);
            appData.setProducts(res.data.results);
            appData.setProductsAmount(res.data.count);
            console.log(res.data.results);
        })
        .catch((err) => console.log(err));
};