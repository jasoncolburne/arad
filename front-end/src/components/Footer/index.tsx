import { Link, useNavigate } from "react-router-dom";
import { emptyState } from "../../datatypes/ApplicationState";
import { useGlobalState } from "../../GlobalState";
import { loggedIn } from "../../utility/authorization";

import "./index.css"


const Footer = () => {
  const { state, setState } = useGlobalState();
  const navigate = useNavigate();

  const logoutAction = (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();
    setState(emptyState);
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
          {loggedIn(state.credentials!) ? logoutLink : null}
        </div>
      </div>
    </footer>
  );
}

export { Footer };
