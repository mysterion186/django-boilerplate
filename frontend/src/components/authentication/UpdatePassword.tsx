/**
 * In this page, the user can update his password
 */
import { useState, FormEvent, ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";

import AuthApi from "../../services/AuthApi";
import AuthStorage from "../../services/AuthStorage";
import { UserPasswordUpdate } from "../../types/api.types";

function UpdatePassword() {
    const [formData, setFormData] = useState<UserPasswordUpdate>({
        old_password: "",
        password: "",
        password1: ""
    });
    
    const navigate = useNavigate();

    const handleSubmit = async (e:FormEvent) => {
        e.preventDefault();
        const token = AuthStorage.getJWTToken() as string;
        const res = await AuthApi.updatePassword(formData, token);
        if (res.status === 200){
            console.log(res);
            navigate("/user");
        }
        else{
            console.log("An error occured ", res);
        }
    }

    const handleInputchange = (e: ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    return(
        <>
        <h1>Updata password pages</h1>
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="old_password">old password</label>
                <div>
                    <input 
                        type="password"
                        id="old_password"
                        name="old_password"
                        value={formData.old_password}
                        onChange={handleInputchange}
                        required
                        placeholder="old password"
                    />
                </div>
                <div>
                    <label htmlFor="password">new password:</label>
                    <input 
                        type="password"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleInputchange}
                        required
                        placeholder="new password"
                    />
                </div>
                <div>
                <label htmlFor="password">new password confirmation:</label>
                    <input 
                        type="password"
                        id="password1"
                        name="password1"
                        value={formData.password1}
                        onChange={handleInputchange}
                        required
                        placeholder="new password confirmation"
                    />
                </div>
            </div>
            <button type="submit">Change password</button>
        </form>
        </>
    )
}

export default UpdatePassword;