import './App.css'
import { Link } from 'react-router-dom';

function App() {
  return (
      <div>
        <h2>React Google Login</h2>
        <p><Link to={"/login"}>login</Link></p>
        <p><Link to={"/register"}>register</Link></p>
        <p><Link to={"/user"}>user</Link></p>
        <p><Link to={"/update-password"}>update-password</Link></p>
        <p><Link to={"/password-reset-link"}>password-reset-link</Link></p>
        <p><Link to={"/optional-field"}>Set optional parameter</Link></p>
        <p>Click on the given link for actually change your password</p>
      </div>
  );
}

export default App;