import api from "../../../api";

export const getCurrentCategoryBrands = (currentCategory, setBrands) => {
    if (currentCategory !== "") {
        api
            .get(`/api/categories/${currentCategory.id}/brands/`)
            .then((res) => {
                console.log(res.data);
                setBrands(res.data);
            })
            .catch((error) => {
                console.log(error);
            });
}};