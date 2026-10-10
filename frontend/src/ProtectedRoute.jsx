import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AppContext } from "./modules/AppProvider/AppProvider";

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useContext(AppContext);

  if (isAuthenticated === null) {
    return <div>Загрузка...</div>;
  }

  if (isAuthenticated === false) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
}

export default ProtectedRoute;
