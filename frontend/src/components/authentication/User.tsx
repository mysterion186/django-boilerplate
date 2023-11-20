/**
 * Quick page in order to display information about the user
 */
import { useState, useEffect } from "react";
import AuthApi from "../../services/AuthApi";
import AuthStorage from "../../services/AuthStorage";
import { UserInformation } from "../../types/api.types";
import { useRequireAuth } from "../../hooks/authentication";
import { useNavigate } from "react-router-dom";

function User() {
    const [user, setUser] = useState<UserInformation>(
        {
            email: "",
            biography: ""
        }
    );
    const navigate = useNavigate();

    useRequireAuth();
    useEffect(() => {
        const fetchData = async () => {
            const token: string = AuthStorage.getJWTToken() as string;
            const response = await AuthApi.getUserInformation(token);

            if (response.status === 200){
                setUser(response.data);
            }
            else if (response.status === 403){
                navigate("/optional-field");
            }
        }
        fetchData();
    }, [])

    return(
        <>
            <div>
                <h1>Congrat's you're logged in !</h1>
                email: {user.email}
                <br />
                biography: {user.biography}
            </div>
        </>
    )
}

export default User;