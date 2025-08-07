import api from "../../../api";

export const getCurrentCategoryBrands = (currentCategory, setBrands) => {
    if (currentCategory !== "") {
        api
            .get(`/api/categories/${currentCategory.id}/brands/`)
            .then((res) => {
                console.log(res.data);

                const brands = res.data.map(brand => {
                    return {id: brand.id, name: brand.name, checked: false};
                });
                setBrands(brands);
                console.log(brands);
            })
            .catch((error) => {
                console.log(error);
            });
}};