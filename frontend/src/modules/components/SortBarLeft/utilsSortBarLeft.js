export const clearFilters = (...fields) => {
    fields.forEach((field) => {
        field.clear();
    });
};