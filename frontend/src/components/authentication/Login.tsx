import { useState, FormEvent, ChangeEvent } from "react";
import { useGoogleLogin } from "@react-oauth/google";

import AuthApi from "../../services/AuthApi";
import { ProviderCredentials, RawProviderCredential } from "../../types/api.types";
import { redirectUser } from "../../utils/AuthUtils";
import { GoogleButton } from "./SocialButton";

function Login() {
    const [formData, setFormData] = useState<{username:string, password: string}>({
        username: '',
        password: '',
    });

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

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        const res = await AuthApi.getJWTToken(formData);
        redirectUser(res);
    };

    const handleInputchange = (e: ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };
    return (
        <>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                    type="text"
                    id="username"
                    name="username"
                    value={formData.username}
                    onChange={handleInputchange}
                    required
                    placeholder="username"
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleInputchange}
                    required
                    placeholder="password"
                    />
                </div>
                <button type="submit">Login</button>
            </form>
            <GoogleButton onClick={LoginFromGoogle}/>
        </>
    )
}

export default Login;