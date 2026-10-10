import { Navigate } from "react-router-dom";
import { AppContext } from "../../AppProvider/AppProvider";
import { logout } from "./apiLogoutPage";
import { useContext, useEffect } from "react";

function LogoutPage() {
  const { setIsAuthenticated } = useContext(AppContext);

  useEffect(() => {
    logout(setIsAuthenticated);
  }, [setIsAuthenticated]);

  return <Navigate to="/login" replace />;
}

export default LogoutPage;
