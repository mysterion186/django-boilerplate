import { useState, useEffect } from 'react'
import './App.css'
import { googleLogout, useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';

interface GoogleLoginResponse {
  access_token: string;
  // Add other properties as needed based on the response structure
}

function App() {
  const [user, setUser] = useState<GoogleLoginResponse | null>(null);
  const [profile, setProfile] = useState<any | null>(null); // You can specify a more specific type for 'profile'

  const  login = useGoogleLogin({
    onSuccess: (codeResponse: GoogleLoginResponse) => {setUser(codeResponse); console.log(
      "user ",user?.access_token,
      "res ", codeResponse
    )},
    onError: (error) => console.log('Login Failed:', error),
  });

  useEffect(() => {
    if (user) {
      axios
        .get(`https://www.googleapis.com/oauth2/v1/userinfo?access_token=${user.access_token}`, {
          headers: {
            Authorization: `Bearer ${user.access_token}`,
            Accept: 'application/json',
          },
        })
        .then((res: any) => {
          setProfile(res.data);
          console.log(res.data);
        })
        .catch((err:any) => console.log(err));
    }
  }, [user]);

  // log out function to log the user out of google and set the profile array to null
  const logOut = () => {
    googleLogout();
    setProfile(null);
  };

  return (
    
      <div>
        <h2>React Google Login</h2>
        <br />
        <br />

        {profile ? (
          <div>
            <img src={profile.picture} alt="user image" />
            <h3>User Logged in</h3>
            <p>Name: {profile.name}</p>
            <p>Email Address: {profile.email}</p>
            <br />
            <br />
            <button onClick={logOut}>Log out</button>
            <button onClick={() => {console.log(user)}}></button>
          </div>
        ) : (
          <button onClick={() => login()}>Sign in with Google 🚀 </button>
        )}
      </div>
  );
}

export default App;