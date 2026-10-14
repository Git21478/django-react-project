import api from "../../../api";

export const getProducts = (
  setProducts,
  setProductsCount,
  currentPage,
  pageSize,
  productsOrdering,
  search = "",
) => {
  api
    .get(
      `products/?pageSize=${pageSize}&page=${currentPage}&ordering=${productsOrdering}&search=${search}`,
    )
    .then((res) => {
      setProducts(res.data.results);
      setProductsCount(res.data.count);
    })
    .catch((error) => console.error(error));
};

export const getCategoryProducts = (
  setProducts,
  setProductsCount,
  currentPage,
  pageSize,
  productsOrdering,
  search = "",
  categoryId = "",
) => {
  api
    .get(
      `catalog/${categoryId}/products/?pageSize=${pageSize}&page=${currentPage}&ordering=${productsOrdering}&search=${search}`,
    )
    .then((res) => {
      setProducts(res.data.results);
      setProductsCount(res.data.count);
    })
    .catch((error) => console.error(error));
};

export const getFilteredProducts = (appData, priceMin, priceMax, brands) => {
  const selectedBrandsIds = brands
    .filter((brand) => brand.checked === true)
    .map((brand) => brand.id);

  let url = `catalog/${appData.currentCategory.id}/products/?pageSize=${appData.pageSize}&page=${appData.currentPage}&ordering=${appData.productsOrdering}&search=${appData.search}`;
  if (priceMin !== "") url += `&price_min=${priceMin}`;
  if (priceMax !== "") url += `&price_max=${priceMax}`;
  if (selectedBrandsIds.length > 0) {
    url += `&selected_brands_ids=${selectedBrandsIds}`;
  }

  api
    .get(url)
    .then((res) => {
      appData.setIsGetFilteredProducts(true);
      appData.setProducts(res.data.results);
      appData.setProductsCount(res.data.count);
    })
    .catch((error) => console.error(error));
};
