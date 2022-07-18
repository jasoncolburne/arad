import { useEffect } from "react";
import { Link } from "react-router-dom";
import { Navigation } from "../../administration/Navigation";
import { ApplicationState } from "../../datatypes/ApplicationState";

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
  const { state, setState } = useGlobalState();

  useEffect(() => {
    const encoded_state: string | null = localStorage.getItem('state');
    if (encoded_state) {
      const state: ApplicationState = JSON.parse(encoded_state);
      setState(state);
    }
  // we only want this to run once
  // eslint-disable-next-line
  }, []);

  return (
    <header className="header">
      <div className="left">
        <Navigation />
      </div>
      <div className="right">
        {loggedIn(state.credentials!) ? clickableEmail(state.user!.email) : authentication}
      </div>
    </header>
  )
}

export { Header };
