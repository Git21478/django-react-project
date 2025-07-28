export const selectCategory = (categories, allBrands, selectedCategoryId, setBrands) => {
    if (selectedCategoryId.value != 0) {
        const selectedCategory = categories.find(el => el.id == selectedCategoryId.value);
        const result = allBrands.filter(el => selectedCategory.brands.includes(el.id));
        setBrands(result);
    } else {
        setBrands(allBrands);
    };
};