import { useState, FormEvent, ChangeEvent } from "react";

import AuthApi from "../../services/AuthApi";
import AuthStorage from "../../services/AuthStorage";
import { useRequireAuth } from "../../hooks/authentication";
import { OptionalUserInformation } from "../../types/api.types";
import { useNavigate } from "react-router-dom";

function UserOptionalField(){
    const [formData, setFormData] = useState<OptionalUserInformation>({
        biography: ""
    });
    const navigate = useNavigate();
    useRequireAuth();

    const handleSubmit = async (e:FormEvent) => {
        e.preventDefault();
        const token:string = AuthStorage.getJWTToken() as string;
        const res = await AuthApi.sendOptional(formData, token);

        if (res.status === 200){
            navigate("/user");
        }
        else{
            console.log("an error occured");
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
        <h1>Set Optional parameter</h1>
            <form onSubmit={handleSubmit}>
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

export default UserOptionalField;