import { Link, useNavigate } from "react-router-dom";
import { User } from "../../datatypes/User";
import { useGlobalState } from "../../GlobalState";

import "./index.css"

const emptyUser: User = {
  roles: [],
  email: '',
}

const Footer = () => {
  const { state, setState } = useGlobalState();
  const navigate = useNavigate();

  const loggedIn = state.user ? state.user.roles.length > 0 : false;

  const logoutAction = (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();

    const newState = { ...state, user: emptyUser };
    setState(newState);

    navigate("/");
  };

  const logoutLink = <Link onClick={logoutAction} to="/logout">Logout</Link>;

  return (
    <footer>
      <div className="footer">
        <div className="left">
          Accessible Research Article Database
        </div>
        <div className="right">
          {loggedIn ? logoutLink : null}
        </div>
      </div>
    </footer>
  );
}

export { Footer };
