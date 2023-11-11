/**
 * In this file there will be all method related to calling authentication API for the 
 * Django (Django Rest Framework) backend. 
 * This may includes some useful methods like getting the JWT Token or creating/loging the user...
 */
import axios from "axios";
import { type_headers, Credentials } from "../types/api.types";

const instance = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL
});

export default {

    async call(method: string, ressources: string, data:object | null = null, token: string | null = null ){
        var headers: type_headers = {
            "Content-type": "application/json"
        };

        if (token !== null){
            headers.authorization = "Bearer " + token;
        }
        return instance({
            method,
            headers: headers,
            url: ressources,
            data
        }).then((res) => {
            return {status: res.status, data: res.data};
        }).catch((err) => {
            return {status: err.response.status, data: err.response.data};
        })
    },

    // call our backend for getting the JWT Token
    getJWTToken(credentials: Credentials){
        var url: string = ""
        if ("access_token" in credentials){
            
            url = `/auth/api/register-by-access-token/social/${credentials.provider}/`
        }
        else {
            url = "not/implemented/yet"
        }
        return this.call("post", url, credentials, null);
    },
}