/**
 * hooks related to the authentication
 */

import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthStorage from "../services/AuthStorage";


function isValideToken (token: string) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    const payload = JSON.parse(jsonPayload);
    if (payload.exp){
        const currentTimestamp = Math.floor(Date.now() / 1000);

        // Check if the token has not expired
        if (payload.exp < currentTimestamp) {
            console.log('Token has expired');
            return false; // Token has expired
        }
        else{
            return true;
        }
    }
    return false;
}

// Basic authentication for the user 
export function useRequireAuth(){
    const navigate = useNavigate();
    useEffect(()=>{
        const token: string | null = AuthStorage.getJWTToken();
        let isAuthenticated: boolean = false;
        if (typeof token !== 'string'){
            isAuthenticated = false; 
        }
        else {
            isAuthenticated = isValideToken(token);
        }
        if(!isAuthenticated){
            navigate("/login");
        }
    }, [navigate]);
}
