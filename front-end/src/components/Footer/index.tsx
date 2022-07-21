import { Link, useNavigate } from "react-router-dom";
import { Api } from "../../api/Api";
import { LogoutRequest, LogoutResponse } from "../../api/types/friendly";
import { emptyState } from "../../datatypes/ApplicationState";
import { useGlobalState } from "../../GlobalState";
import { loggedIn } from "../../utility/authorization";

import "./index.css"


const Footer = () => {
  const { state, setState } = useGlobalState();
  const navigate = useNavigate();

  const resetStateAndRedirectHome = () => {
    setState(emptyState);
    navigate("/");
  };

  const handleErrors = (response: Response) => {
    if ([401, 403].includes(response.status)) {
      resetStateAndRedirectHome();
    } else {
      // TODO think about this
      resetStateAndRedirectHome();
    }
  };

  const logoutAction = async (event: React.MouseEvent<HTMLAnchorElement>) => {
    event.preventDefault();

    const request: LogoutRequest = { refresh_token: state.credentials!.refresh_token };
    const response: LogoutResponse = await Api().post('identify/logout', null, request, handleErrors);

    resetStateAndRedirectHome();
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
