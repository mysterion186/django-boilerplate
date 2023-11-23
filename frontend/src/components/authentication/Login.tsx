import { useState, FormEvent, ChangeEvent } from "react";
import { useGoogleLogin } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";

import AuthApi from "../../services/AuthApi";
import AuthStorage from "../../services/AuthStorage";
import { BasicCredentials, ProviderCredentials, RawProviderCredential, RawProviderCredentialCamelCase } from "../../types/api.types";
import { GoogleButton } from "./SocialButton";
import FacebookLogin from '@greatsumini/react-facebook-login';


function Login() {
    const [formData, setFormData] = useState<BasicCredentials>({
        email: '',
        password: '',
    });
    const navigate = useNavigate();

    const LoginFromGoogle = useGoogleLogin({
        onSuccess: async (codeResponse: RawProviderCredential) => {
            const formattedCredentials: ProviderCredentials = {
                access_token: codeResponse.access_token,
                provider: "google-oauth2"
            };
            const res = await AuthApi.getJWTToken(formattedCredentials);
            if (res.status === 200){
                AuthStorage.saveJWTToken(res.data.access);
                navigate("/user");
            }
            else{
                console.log("An error occured ", res);
            }
            
        },
        onError: (error) => {
            console.log("Login Failed ", error);
        }
    })

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        const res = await AuthApi.getJWTToken(formData);
        if (res.status === 200){
            console.log(res.data.access)
            AuthStorage.saveJWTToken(res.data.access);
            navigate("/user");
        }
        else{
            console.log("An error occured ", res);
        }
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
                    <label htmlFor="email">email:</label>
                    <input
                    type="text"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputchange}
                    required
                    placeholder="email"
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
            <br />
            <FacebookLogin
                appId={import.meta.env.VITE_FACEBOOK_APP_ID}
                fields="email"
                style={{
                    backgroundColor: '#4267b2',
                    color: '#fff',
                    fontSize: '16px',
                    padding: '12px 24px',
                    border: 'none',
                    borderRadius: '8px',
                  }}
                onSuccess={async (response: RawProviderCredentialCamelCase) => {
                    const formattedCredentials: ProviderCredentials = {
                        access_token: response.accessToken,
                        provider: "facebook"
                    };
                    const res = await AuthApi.getJWTToken(formattedCredentials);
                    if (res.status === 200){
                        AuthStorage.saveJWTToken(res.data.access);
                        navigate("/user");
                    }
                    else{
                        console.log("An error occured ", res);
                    }
                }}
                onFail={(error) => {
                    console.log('Login Failed!', error);
                }}
            />
        </>
    )
}

export default Login;