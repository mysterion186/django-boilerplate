import { FormEvent } from "react";
import PaymentApi from "../../services/PaymentApi";

function Subscription() {

    const handleSubmit =async (e: FormEvent) => {
        e.preventDefault();
        console.log("There is the request to send", {
            "price_id": "price_1OQxwTJxBksF9wytzb7lk3Gq"
        });
        const res = await PaymentApi.createSubscription({
            "price_id": "price_1OQxwTJxBksF9wytzb7lk3Gq"
        });
        console.log("result", res);
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