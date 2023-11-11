import { useGoogleLogin } from "@react-oauth/google";
import AuthApi from "../../services/AuthApi";
import { ProviderCredentials, RawProviderCredential } from "../../types/api.types";

interface GoogleLoginResponse {
    access_token: string;
}

function Login() {

    const LoginFromGoogle = useGoogleLogin({
        onSuccess: (codeResponse: RawProviderCredential) => {
            const formattedCredentials: ProviderCredentials = {
                access_token: codeResponse.access_token,
                provider: "google-oauth2"
            };
            console.log("raw response ", codeResponse, "formatted response ", formattedCredentials);
            const res = AuthApi.getJWTToken(formattedCredentials);
            console.log("There is the result ", res);
            console.log("Based on the status, I need to redirect the user now to the correct page");
            
        },
        onError: (error) => {
            console.log("Login Failed ", error);
        }
    })

    return (
        <>
            <form action="">
                <input type="text" placeholder="Email"/>
                <input type="password" placeholder="Password"/>
            </form>
            <button>Login</button>
            <button onClick={() => {LoginFromGoogle()}}>Continue with Google</button>
        </>
    )
}

export default Login;