import api from "../../../api";

export const getCategories = (setCategories) => {
  api
    .get("categories/")
    .then((res) => {
      setCategories(res.data);
    })
    .catch((error) => console.error(error));
};

export const getCategoryName = (categorySlug, setCategoryName) => {
  api
    .get("categories/")
    .then((res) => {
      const categories = res.data;
      const categoryName = categories.find(
        (category) => category.slug === categorySlug,
      ).name;
      setCategoryName(categoryName);
    })
    .catch((error) => console.error(error));
};
