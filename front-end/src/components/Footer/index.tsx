import { Link } from "react-router-dom"; 

import type { User } from "../../datatypes/User";

import "./index.css"

const logout = <Link to='/logout'>Logout</Link>;

const Footer = () => {
  const user: User = {
    roles: [],
    email: '',
  }
  
  const loggedIn = user.roles.length > 0;

  return (
    <footer>
      <div className="footer">
        <div className="left">
          Accessible Research Article Database
        </div>
        <div className="right">
          {loggedIn ? logout : null}
        </div>
      </div>
    </footer>
  );
}

export { Footer };
