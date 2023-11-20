/**
 * In this file there will be all method related to calling authentication API for the 
 * Django (Django Rest Framework) backend. 
 * This may includes some useful methods like getting the JWT Token or creating/loging the user...
 */
import axios from "axios";
import { type_headers, Credentials, UserRegistration, UserPasswordUpdate, OptionalUserInformation } from "../types/api.types";

const instance = axios.create({
    baseURL: import.meta.env.VITE_BACKEND_URL
});

export default {

    async call(method: string, ressources: string, data:object | null = null, token: string | null = null ){
        const headers: type_headers = {
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
    async getJWTToken(credentials: Credentials){
        let url: string = ""
        if ("access_token" in credentials){
            
            url = `/auth/register-by-access-token/social/${credentials.provider}/`
        }
        else {
            url = "auth/token"
        }
        return await this.call("post", url, credentials, null);
    },

    // register a basic user
    async registerBasicUser(data:UserRegistration){
        return await this.call("post","/auth/create-user", data);
    },

    // get User's information
    async getUserInformation(token: string){
        return await this.call("get", "/auth/user", null, token);
    },

    // let user update it's password
    async updatePassword(data: UserPasswordUpdate, token:string){
        return await this.call("put", "/auth/update-password", data, token);
    },

    // send a reset password link to the provided email
    async sendResetPasswordLink(data: {email:string}){
        return await this.call("post", "/auth/password-reset-link", data);
    },

    // form for actually resetting the password
    async sendPassword(data: {password:string, password1:string, token:string, uidb64: string}){
        return await this.call("post", "/auth/reset-password", data);
    },

    // send all the optional field of the user (either the first time or for updating)
    async sendOptional(data: OptionalUserInformation, token:string){
        return await this.call("put", "/auth/set-optional", data, token);
    }
}