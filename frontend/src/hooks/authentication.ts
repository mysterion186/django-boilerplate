/**
 * hooks related to the authentication
 */

import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecrypt } from 'jose';
import AuthStorage from "../services/AuthStorage";


function isTokenValid(token: string): boolean {
    try {
      const { payload } = { jwtDecrypt }.decode(token, { complete: true });
  
      if (!payload || !payload.exp) {
        return false; // Invalid token format
      }
  
      const currentTimestamp = Math.floor(Date.now() / 1000);
      return currentTimestamp < payload.exp;
    } catch (error) {
      return false; // Token decoding or verification failed
    }
}

export function useRequireAuth(){
    const navigate = useNavigate();

    useEffect(()=>{
        const token: string | null = AuthStorage.getJWTToken();
        let isAuthenticated:boolean;
        if (typeof token !== 'string'){
            isAuthenticated = false; 
        }
        else {
            isAuthenticated = isTokenValid(token);
        }
    
        if(!isAuthenticated){
            // navigate("/login");
            console.log("Please log in !")
        }
    }, []);
}