import { createBrowserRouter } from "react-router-dom";
import App from './App.tsx'
import Login from "./components/authentication/Login.tsx";
import Registration from "./components/authentication/Registration.tsx";

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />
    },
    {
        path: "login",
        element: <Login />
    },
    {
        path: "register",
        element: <Registration />
    }
])

export default router;