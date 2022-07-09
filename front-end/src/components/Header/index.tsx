import { Link } from "react-router-dom";
import { Navigation } from "../../administration/Navigation";

import { useGlobalState } from "../../GlobalState";

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
  const { state } = useGlobalState();
  const loggedIn = state.user ? state.roles!.length > 0 : false;

  return (
    <header className="header">
      <div className="left">
        {/* TODO: when not an admin, don't display this */}
        <Navigation />
      </div>
      <div className="right">
        {loggedIn ? clickableEmail(state.user!.email) : authentication}
      </div>
    </header>
  )
}

export { Header };
