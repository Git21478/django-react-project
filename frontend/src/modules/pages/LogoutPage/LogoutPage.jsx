import { Navigate } from "react-router-dom";
import { AppContext } from "../../AppProvider/AppProvider";
import { logout } from "./apiLogoutPage";
import { useContext, useEffect } from "react";

function LogoutPage() {
  const { setUser, setIsAuthenticated } = useContext(AppContext);

  useEffect(() => {
    logout(setUser, setIsAuthenticated);
  }, [setIsAuthenticated]);

  return <Navigate to="/login" replace />;
}

export default LogoutPage;
