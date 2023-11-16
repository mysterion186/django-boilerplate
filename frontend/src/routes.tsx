import { createBrowserRouter } from "react-router-dom";
import App from './App.tsx'
import Login from "./components/authentication/Login.tsx";
import Registration from "./components/authentication/Registration.tsx";
import User from "./components/authentication/User.tsx";

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
    },
    {
        path: "user",
        element: <User />
    }
])

export default router;