import React, { useEffect, useState } from "react";
import { getCategoryProducts, getProducts } from "../pages/HomePage/apiHomePage";
import { getCategories } from "../components/Sidebar/apiSidebar";
import { createPages } from "./utilsAppProvider";
import { auth } from "./apiAppProvider";
import { getAvatar } from "../components/Header/HeaderRight/apiHeaderRight";

export const AppContext = React.createContext();

function AppProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(null);
    const [isGetFilteredProducts, setIsGetFilteredProducts] = useState(false);
    const [categories, setCategories] = useState("");
    const [currentCategorySlug, setCurrentCategorySlug] = useState("");
    const [currentCategory, setCurrentCategory] = useState("");
    const [openCatalog, setOpenCatalog] = useState(false);
    const [openUserMenu, setOpenUserMenu] = useState(false);
    const [productsAmount, setProductsAmount] = useState(0);
    const [productsOrdering, setProductsOrdering] = useState("price");
    const [reviewsOrdering, setReviewsOrdering] = useState("created_at");
    const [products, setProducts] = useState([]);
    const [favoriteProducts, setFavoriteProducts] = useState([]);
    const [cartProductsObject, setCartProductsObject] = useState({cart_products: [], total_quantity: 0, total_price: 0});
    const pageSize = 10;
    const [currentPage, setCurrentPage] = useState(1);
    const [pages, setPages] = useState([1]);
    const [search, setSearch] = useState("");
    const [avatar, setAvatar] = useState("");

    const contextObject = {
        isAuthenticated: isAuthenticated,
        isGetFilteredProducts: isGetFilteredProducts,
        categories: categories,
        currentCategorySlug: currentCategorySlug,
        currentCategory: currentCategory,
        openCatalog: openCatalog,
        openUserMenu: openUserMenu,
        productsAmount: productsAmount,
        productsOrdering: productsOrdering,
        reviewsOrdering: reviewsOrdering,
        products: products,
        favoriteProducts: favoriteProducts,
        cartProductsObject: cartProductsObject,
        currentPage: currentPage,
        pageSize: pageSize,
        pages: pages,
        search: search,
        avatar: avatar,

        setIsAuthenticated: setIsAuthenticated,
        setIsGetFilteredProducts: setIsGetFilteredProducts,
        setCategories: setCategories,
        setCurrentCategorySlug: setCurrentCategorySlug,
        setCurrentCategory: setCurrentCategory,
        setOpenCatalog: setOpenCatalog,
        setOpenUserMenu: setOpenUserMenu,
        setProductsAmount: setProductsAmount,
        setProductsOrdering: setProductsOrdering,
        setReviewsOrdering: setReviewsOrdering,
        setProducts: setProducts,
        setFavoriteProducts: setFavoriteProducts,
        setCartProductsObject: setCartProductsObject,
        setCurrentPage: setCurrentPage,
        setPages: setPages,
        setSearch: setSearch,
        setAvatar: setAvatar,
    };

    useEffect(() => {
        auth(setIsAuthenticated);
        getCategories(setCategories);
    }, []);

    useEffect(() => {
        isAuthenticated && getAvatar(setAvatar);
    }, [isAuthenticated]);

    useEffect(() => {
        createPages(productsAmount, pageSize, setPages);
    }, [productsAmount]);
    
    useEffect(() => {
        categories !== "" && setCurrentCategory(categories.find(category => category.slug === currentCategorySlug));
    }, [categories]);

    useEffect(() => {
        !currentCategory
            ? getProducts(setProducts, setProductsAmount, currentPage, pageSize, productsOrdering, search)
            : !isGetFilteredProducts
                ? getCategoryProducts(setProducts, setProductsAmount, currentPage, pageSize, productsOrdering, search, currentCategory.id)
                : setIsGetFilteredProducts(false);
    }, [currentPage, productsOrdering, productsAmount, currentCategory, cartProductsObject]);
    
    return (
        <>
            <AppContext.Provider value={contextObject}>
                {children}
            </AppContext.Provider>
        </>
    );
};

export default AppProvider;