/**
 * Quick page in order to display information about the user
 */
import { useState, useEffect } from "react";
import AuthApi from "../../services/AuthApi";
import AuthStorage from "../../services/AuthStorage";
import { UserInformation } from "../../types/api.types";
import { useRequireAuth } from "../../hooks/authentication";

function User() {
    const [user, setUser] = useState<UserInformation>(
        {
            email: "",
            biography: ""
        }
    );
    useRequireAuth();
    useEffect(() => {
        const fetchData = async () => {
            const token: string = AuthStorage.getJWTToken() as string;
            const response = await AuthApi.getUserInformation(token);

            if (response.status === 200){
                setUser(response.data);
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