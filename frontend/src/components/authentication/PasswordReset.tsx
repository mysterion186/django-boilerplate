/**
 * View where the user's reset it's password.
 * To get to this pages, the user should have clicked on the link sent on his email
 */

import { useState, FormEvent, ChangeEvent } from "react";
import { useParams, useNavigate } from "react-router-dom";

import AuthApi from "../../services/AuthApi";

function PasswordReset() {
    const navigate = useNavigate();
    const {uidb64, token} = useParams();
    const [formData, setFormData] = useState<{password:string, password1: string}>({
        password:"",
        password1:""
    });

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        const data = {
            "password": formData.password,
            "password1": formData.password1,
            "uidb64": uidb64 as string,
            "token": token as string
        }
        const res = await AuthApi.sendPassword(data);
        if (res.status === 200){
            console.log(res);
        }
        else{
            console.log(res);
        }

    };

    const handleInputchange = (e: ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    return(
        <>
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="password">password:</label>
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
            <div>
                <label htmlFor="password">Password:</label>
                <input
                type="password"
                id="password1"
                name="password1"
                value={formData.password1}
                onChange={handleInputchange}
                required
                placeholder="password confirmation"
                />
            </div>
            <button type="submit">Reset Password</button>
        </form>
        </>
    )
}

export default PasswordReset;