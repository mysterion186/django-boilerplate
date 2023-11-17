/**
 * Page asking for an email.
 * We'll send a reset password link to the provided email
*/
import { useState, FormEvent, ChangeEvent } from "react";
import AuthApi from "../../services/AuthApi";

function PasswordResetLink() {
    const [email, setEmail] = useState<string>("");
    
    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        const res = await AuthApi.sendResetPasswordLink({"email": email});
        if (res.status === 201){
            console.log(res);
        }
        else{
            console.log(res);
        }
    };

    const handleInputchange = (e: ChangeEvent<HTMLInputElement>) => {
        console.log(email);
        const {value} = e.target;
        setEmail(value);
    };

    return(
        <>
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="email">email:</label>
                <input
                type="text"
                id="email"
                name="email"
                value={email}
                onChange={handleInputchange}
                required
                placeholder="email"
                />
            </div>
            <button type="submit">Login</button>
        </form>
        </>
    )
}

export default PasswordResetLink;