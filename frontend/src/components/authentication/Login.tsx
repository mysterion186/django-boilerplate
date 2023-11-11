import { useGoogleLogin } from "@react-oauth/google";
import AuthApi from "../../services/AuthApi";
import { ProviderCredentials, RawProviderCredential } from "../../types/api.types";
import { redirectUser } from "../../utils/AuthUtils";

function Login() {

    const LoginFromGoogle = useGoogleLogin({
        onSuccess: async (codeResponse: RawProviderCredential) => {
            const formattedCredentials: ProviderCredentials = {
                access_token: codeResponse.access_token,
                provider: "google-oauth2"
            };
            const res = await AuthApi.getJWTToken(formattedCredentials);
            redirectUser(res);
            
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