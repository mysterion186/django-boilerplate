import { createBrowserRouter } from "react-router-dom";
import App from './App.tsx'
import Login from "./components/authentication/Login.tsx";
import Registration from "./components/authentication/Registration.tsx";
import User from "./components/authentication/User.tsx";
import UpdatePassword from "./components/authentication/UpdatePassword.tsx";
import PasswordResetLink from "./components/authentication/PasswordResetLink.tsx";
import PasswordReset from "./components/authentication/PasswordReset.tsx";
import UserOptionalField from "./components/authentication/UserOptionalField.tsx";
import Subscription from "./components/payments/Subscription.tsx";
import Cancel from "./components/payments/Cancel.tsx";
import Success from "./components/payments/Success.tsx";

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
    },
    {
        path: "update-password",
        element: <UpdatePassword />
    },
    {
        path: "password-reset-link",
        element: <PasswordResetLink />
    },
    {
        path: "password/reset/:uidb64/:token",
        element: <PasswordReset />
    },
    {
        path: "optional-field",
        element: <UserOptionalField />
    },
    {
        path: "payment",
        element: <Subscription />
    },
    {
        path: "payment/cancel",
        element: <Cancel />
    },
    {
        path: "payment/success",
        element: <Success />
    }
])

export default router;