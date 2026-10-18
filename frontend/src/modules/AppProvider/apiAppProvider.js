import api from "../../api";

export const getUser = (setUser, setIsAuthenticated) => {
  api
    .get("user/me/")
    .then((res) => {
      setUser(res.data);
      setIsAuthenticated(true);
    })
    .catch((_) => {
      setUser(null);
      setIsAuthenticated(false);
    });
};

export const getProducts = (params, { setProducts, setProductsCount }) => {
  const query = new URLSearchParams();

  if (params.page != null) query.set("page", params.page);
  if (params.pageSize != null) query.set("page_size", params.pageSize);
  if (params.ordering) query.set("ordering", params.ordering);
  if (params.search) {
    query.set("search", params.search);
  }
  if (params.categoryId !== "" && params.categoryId != null) {
    query.set("category_id", params.categoryId);
  }
  if (params.priceMin !== "" && params.priceMin != null) {
    query.set("price_min", params.priceMin);
  }
  if (params.priceMax !== "" && params.priceMax != null) {
    query.set("price_max", params.priceMax);
  }
  if (params.brandIds?.length) {
    query.set("brand_ids", params.brandIds.join(","));
  }

  return api
    .get(`products/?${query.toString()}`)
    .then((res) => {
      setProducts(res.data.results);
      setProductsCount(res.data.count);
    })
    .catch((error) => {
      console.error(error);
    });
};
