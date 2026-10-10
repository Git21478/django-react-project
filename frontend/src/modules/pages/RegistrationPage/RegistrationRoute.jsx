import RegistrationPage from "./RegistrationPage";
import { useContext } from "react";
import { Navigate } from "react-router-dom";

function RegistrationRoute() {
  const { isAuthenticated } = useContext(AppContext);
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  return <RegistrationPage />;
}

export default RegistrationRoute;
