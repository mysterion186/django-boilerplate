import axios from "axios";
import { type_headers } from "../types/api.types";

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

    // create subscription
    async createSubscription(subscriptionData: object){
        return await this.call("post", "/payments/create-subscription", subscriptionData);
    }
}