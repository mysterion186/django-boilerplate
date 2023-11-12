import { useState, FormEvent, ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";

import AuthApi from "../../services/AuthApi";
import { UserRegistration } from "../../types/api.types";

function Registration() {
    const [formData, setFormData] = useState<UserRegistration>({
        email: "",
        password: "",
        password1: "",
        biography: "",
    });
    const navigate = useNavigate();

    const handleSubmit = async (e:FormEvent) => {
        e.preventDefault();
        const res = await AuthApi.registerBasicUser(formData);
        if (res.status === 200){
            navigate("/");
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
        <h1>Registration page</h1>
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
                <div>
                    <label htmlFor="password1">Password Confirmation:</label>
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
                <div>
                    <label htmlFor="biography">biography:</label>
                    <input
                    type="text"
                    id="biography"
                    name="biography"
                    value={formData.biography}
                    onChange={handleInputchange}
                    required
                    placeholder="biography"
                    />
                </div>
                <button type="submit">Register</button>
            </form>
        </>
    )
}

export default Registration;
