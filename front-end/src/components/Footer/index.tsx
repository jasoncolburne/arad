import { Link, useNavigate } from "react-router-dom";
import { User } from "../../api/types/friendly";
import { useGlobalState } from "../../GlobalState";
import { loggedIn } from "../../utility/authorization";

import "./index.css"

const emptyUser: User = {
  id: '',
  email: '',
}

const Footer = () => {
  const { state, setState } = useGlobalState();
  const navigate = useNavigate();

  const logoutAction = (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();

    // wait do we actually need to have this ...state here?
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
          {loggedIn(state) ? logoutLink : null}
        </div>
      </div>
    </footer>
  );
}

export { Footer };
