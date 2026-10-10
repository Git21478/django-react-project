import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProductPage from "./modules/pages/ProductPage/ProductPage";
import LoginPage from "./modules/pages/LoginPage/LoginPage";
import LogoutPage from "./modules/pages/LogoutPage/LogoutPage";
import NotFoundPage from "./modules/pages/NotFoundPage/NotFoundPage";
import ProfilePage from "./modules/pages/ProfilePage/ProfilePage";
import RegistrationRoute from "./modules/pages/RegistrationPage/RegistrationRoute";
import PasswordResetPage from "./modules/pages/PasswordResetPages/PasswordResetPage/PasswordResetPage";
import PasswordResetConfirm from "./modules/pages/PasswordResetPages/PasswordResetConfirmPage/PasswordResetConfirmPage";
import CartPage from "./modules/pages/CartPage/CartPage";
import CategoryPage from "./modules/pages/CategoryPage/CategoryPage";
import HomePage from "./modules/pages/HomePage/HomePage";
import ProtectedRoute from "./ProtectedRoute";
import AppProvider from "./modules/AppProvider/AppProvider";
import FavoritesPage from "./modules/pages/FavoritesPage/FavoritesPage";

function App() {
  return (
    <BrowserRouter
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <AppProvider>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/catalog/:category_slug" element={<CategoryPage />} />
          <Route path="/products/:product_id" element={<ProductPage />} />
          <Route path="/favorites" element={<FavoritesPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/logout" element={<LogoutPage />} />
          <Route path="/registration" element={<RegistrationRoute />} />
          <Route path="/password-reset" element={<PasswordResetPage />} />
          <Route
            path="/password-reset/confirm"
            element={<PasswordResetConfirm />}
          />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </AppProvider>
    </BrowserRouter>
  );
}

export default App;
