import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ProductPage from "./modules/pages/ProductPage/ProductPage";
import LoginPage from "./modules/pages/LoginPage/LoginPage";
import RegistrationPage from "./modules/pages/RegistrationPage/RegistrationPage";
import NotFoundPage from "./modules/pages/NotFoundPage/NotFoundPage";
import ProfilePage from "./modules/pages/ProfilePage/ProfilePage";
import PasswordResetPage from "./modules/pages/PasswordResetPages/PasswordResetPage/PasswordResetPage";
import PasswordResetDone from "./modules/pages/PasswordResetPages/PasswordResetDonePage/PasswordResetDonePage";
import PasswordResetConfirm from "./modules/pages/PasswordResetPages/PasswordResetConfirmPage/PasswordResetConfirmPage";
import PasswordResetComplete from "./modules/pages/PasswordResetPages/PasswordResetCompletePage/PasswordResetCompletePage";
import CartPage from "./modules/pages/CartPage/CartPage";
import CategoryPage from "./modules/pages/CategoryPage/CategoryPage";
import HomePage from "./modules/pages/HomePage/HomePage";
import ProtectedRoute from "./ProtectedRoute";
import AppProvider from "./modules/AppProvider/AppProvider";
import FavoritesPage from "./modules/pages/FavoritesPage/FavoritesPage";

function Logout() {
    localStorage.clear();
    return <Navigate to="/login"/>;
};

function RegisterAndLogout() {
    localStorage.clear();
    return (
        <AppProvider>
            <RegistrationPage/>
        </AppProvider>
    );
};

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={
                    <AppProvider>
                        <HomePage/>
                    </AppProvider>
                }/>
                <Route path="/catalog/:category_slug" element={
                    <AppProvider>
                        <CategoryPage/>
                    </AppProvider>
                }/>
                <Route path="/products/:product_id" element={
                    <AppProvider>
                        <ProductPage/>
                    </AppProvider>
                }/>
                <Route path="/favorites" element={
                    <AppProvider>
                        <FavoritesPage/>
                    </AppProvider>
                }/>
                <Route path="/cart" element={
                    <AppProvider>
                        <CartPage/>
                    </AppProvider>
                }/>
                <Route path="/profile" element={
                    <AppProvider>
                        <ProtectedRoute>
                            <ProfilePage/>
                        </ProtectedRoute>
                    </AppProvider>
                }/>
                <Route path="/login" element={
                    <AppProvider>
                        <LoginPage/>
                    </AppProvider>
                }/>
                <Route path="/logout" element={<Logout/>}/>
                <Route path="/registration" element={<RegisterAndLogout/>}/>

                <Route path="/password-reset" element={
                    <AppProvider>
                        <PasswordResetPage/>
                    </AppProvider>
                }/>
                <Route path="/password-reset-done" element={<PasswordResetDone/>}/>
                <Route path="/password-reset-confirm/:uidb64/:token" element={<PasswordResetConfirm/>}/>
                <Route path="/password-reset-complete" element={<PasswordResetComplete/>}/>
                
                <Route path="*" element={<NotFoundPage/>}/>
            </Routes>
        </BrowserRouter>
    );
};

export default App;