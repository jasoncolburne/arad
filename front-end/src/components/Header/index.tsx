import { Link } from "react-router-dom";
import { Navigation } from "../../administration/Navigation";

import type { User } from "../../datatypes/User";

import "./index.css"

const authentication = (
  <>
    <Link to="/login">Login</Link>{" / "}
    <Link to="/register">Register</Link>
  </>
);

const clickableEmail = (email: string) => {
  return <Link to="/passphrase">{email}</Link>;
}

const Header = () => {
  const user: User = {
    roles: [],
    email: '',
  }
  
  const loggedIn = user.roles.length > 0;

  return (
    <header className="header">
      <div className="left">
        {/* TODO: when not an admin, don't display this */}
        <Navigation />
      </div>
      <div className="right">
        {loggedIn ? clickableEmail(user.email) : authentication}
      </div>
    </header>
  )
}

export { Header };
