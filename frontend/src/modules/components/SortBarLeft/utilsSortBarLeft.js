export const handleCheckboxChange = (id, setBrands) => {
  setBrands((prev) =>
    prev.map((brand) =>
      brand.id === id ? { ...brand, checked: !brand.checked } : brand,
    ),
  );
};

export const applyFilters = ({
  getProducts,
  appData,
  page = 1,
  priceMin = "",
  priceMax = "",
  brandIds = [],
} = {}) => {
  getProducts(
    {
      page,
      pageSize: appData.pageSize,
      ordering: appData.productsOrdering,
      search: appData.search,
      categoryId: appData.currentCategory?.id,
      priceMin,
      priceMax,
      brandIds,
    },
    {
      setProducts: appData.setProducts,
      setProductsCount: appData.setProductsCount,
    },
  );
};

export const clearFilters = (priceMin, priceMax, setBrands, setCurrentPage) => {
  priceMin.clear();
  priceMax.clear();
  setBrands((prev) => prev.map((brand) => ({ ...brand, checked: false })));
  setCurrentPage(1);
};
