import api from "../../../api";

export const getCategories = (setCategories) => {
    api
        .get("/api/categories/")
        .then((res) => {
            setCategories(res.data);
            console.log("CATEGORIES", res.data);
        })
        .catch((err) => console.log(err));
};

export const getCategoryName = (categorySlug, setCategoryName) => {
    api
        .get("/api/categories/")
        .then((res) => {
            const categories = res.data;
            console.log(categories);
            const categoryName = categories.find(category => category.slug === categorySlug).name;
            setCategoryName(categoryName);
        })
        .catch((err) => console.log(err));
};