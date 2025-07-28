import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AppContext } from "./modules/AppProvider/AppProvider";

function ProtectedRoute({ children }) {
    const appData = useContext(AppContext);
    
    if (appData.isAuthenticated === null) {
        return <div>Загрузка...</div>
    };

    if (appData.isAuthenticated === false) {
        return <Navigate to="/login"/>
    };

    return (
        <>
            {children}
        </>
    );
};

export default ProtectedRoute;