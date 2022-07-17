import { Link } from "react-router-dom";
import { Navigation } from "../../administration/Navigation";

import { useGlobalState } from "../../GlobalState";
import { loggedIn } from "../../utility/authorization";

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

  return (
    <header className="header">
      <div className="left">
        {/* TODO: when not an admin, don't display this */}
        <Navigation />
      </div>
      <div className="right">
        {loggedIn(state.credentials!) ? clickableEmail(state.user!.email) : authentication}
      </div>
    </header>
  )
}

export { Header };
