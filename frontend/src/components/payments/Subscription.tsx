import { FormEvent } from "react";
import PaymentApi from "../../services/PaymentApi";
import { useRequireAuth } from "../../hooks/authentication";
import AuthStorage from "../../services/AuthStorage";

function Subscription() {

    useRequireAuth();
    const handleSubmit =async (e: FormEvent) => {
        e.preventDefault();
        console.log("There is the request to send", {
            "price_id": "price_1OQxwTJxBksF9wytzb7lk3Gq"
        });
        const token: string = AuthStorage.getJWTToken() as string;
        const res = await PaymentApi.createSubscription({
            "price_id": "price_1OQxwTJxBksF9wytzb7lk3Gq"
        }, token);
        if (res.status === 303){
            const url: string = res.data["url"];
            window.location.href = url;
        }
    }
    return(
        <>
            <h1>Subscription page: </h1>
            <form onSubmit={handleSubmit}>
                <button type="submit">Buy</button>
            </form>
        </>
    )
}

export default Subscription;