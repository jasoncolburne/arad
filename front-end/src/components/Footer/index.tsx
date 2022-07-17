import { Link, useNavigate } from "react-router-dom";
import { User } from "../../api/types/friendly";
import { useGlobalState } from "../../GlobalState";

import "./index.css"

const emptyUser: User = {
  id: '',
  email: '',
}

const Footer = () => {
  const { state, setState } = useGlobalState();
  const navigate = useNavigate();

  const loggedIn = state.roles!.length > 0;

  const logoutAction = (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();

    const newState = { ...state, user: emptyUser, roles: [] };
    setState(newState);

    navigate("/");
  };

  const logoutLink = <Link onClick={logoutAction} to="/logout">Logout</Link>;

  return (
    <footer>
      <div className="footer">
        <div className="left">
          <Link to="/code">Accessible Research Article Database</Link>
        </div>
        <div className="right">
          {loggedIn ? logoutLink : null}
        </div>
      </div>
    </footer>
  );
}

export { Footer };
