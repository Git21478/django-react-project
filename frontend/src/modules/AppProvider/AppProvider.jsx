import React, { useEffect, useState } from "react";
import {
  getCategoryProducts,
  getProducts,
} from "../pages/HomePage/apiHomePage";
import { getCategories } from "../components/Sidebar/apiSidebar";
import { createPages } from "./utilsAppProvider";
import { getUser } from "./apiAppProvider";
import { getProfile } from "../pages/ProfilePage/apiProfilePage";

export const AppContext = React.createContext();

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const [profile, setProfile] = useState("");
  const [isGetFilteredProducts, setIsGetFilteredProducts] = useState(false);
  const [categories, setCategories] = useState([]);
  const [currentCategorySlug, setCurrentCategorySlug] = useState("");
  const [currentCategory, setCurrentCategory] = useState(null);
  const [openCatalog, setOpenCatalog] = useState(false);
  const [openUserMenu, setOpenUserMenu] = useState(false);
  const [productsCount, setProductsCount] = useState(0);
  const [productsOrdering, setProductsOrdering] = useState("price");
  const [reviewsOrdering, setReviewsOrdering] = useState("created_at");
  const [products, setProducts] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [cart, setCart] = useState({
    cart_products: [],
    total_quantity: 0,
    total_price: 0,
  });
  const pageSize = 10;
  const [currentPage, setCurrentPage] = useState(1);
  const [pages, setPages] = useState([1]);
  const [search, setSearch] = useState("");

  const contextObject = {
    user,
    isAuthenticated,
    profile,
    isGetFilteredProducts,
    categories,
    currentCategorySlug,
    currentCategory,
    openCatalog,
    openUserMenu,
    productsCount,
    productsOrdering,
    reviewsOrdering,
    products,
    favorites,
    cart,
    currentPage,
    pageSize,
    pages,
    search,

    setUser,
    setIsAuthenticated,
    setProfile,
    setIsGetFilteredProducts,
    setCategories,
    setCurrentCategorySlug,
    setCurrentCategory,
    setOpenCatalog,
    setOpenUserMenu,
    setProductsCount,
    setProductsOrdering,
    setReviewsOrdering,
    setProducts,
    setFavorites,
    setCart,
    setCurrentPage,
    setPages,
    setSearch,
  };

  useEffect(() => {
    getUser(setUser, setIsAuthenticated);
    getCategories(setCategories);
  }, []);

  useEffect(() => {
    isAuthenticated && getProfile(setProfile);
  }, [isAuthenticated]);

  useEffect(() => {
    createPages(productsCount, pageSize, setPages);
  }, [productsCount]);

  useEffect(() => {
    setCurrentCategory(
      categories.find((category) => category.slug === currentCategorySlug),
    );
  }, [categories, currentCategorySlug]);

  useEffect(() => {
    !currentCategory
      ? getProducts(
          setProducts,
          setProductsCount,
          currentPage,
          pageSize,
          productsOrdering,
          search,
        )
      : !isGetFilteredProducts
        ? getCategoryProducts(
            setProducts,
            setProductsCount,
            currentPage,
            pageSize,
            productsOrdering,
            search,
            currentCategory.id,
          )
        : setIsGetFilteredProducts(false);
  }, [
    currentPage,
    productsOrdering,
    currentCategory?.id,
  ]);

  return (
    <>
      <AppContext.Provider value={contextObject}>
        {children}
      </AppContext.Provider>
    </>
  );
}

export default AppProvider;
