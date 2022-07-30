import { Link } from "react-router-dom";

import { useGlobalState } from "../../../GlobalState";
import { isAdministrator } from "../../../utility/authorization";

const adminLinks = (
  <>
    {" / "}
    <Link id="arad-articlesLink" to="/articles">
      Manage Articles
    </Link>
    {" / "}
    <Link id="arad-usersLink" to="/users">
      Manage Users
    </Link>
  </>
);

const Navigation = () => {
  const { state } = useGlobalState();

  return (
    <header>
      <nav>
        <Link to="/search">Search</Link>
        {state.user !== undefined && isAdministrator(state.user.roles)
          ? adminLinks
          : null}
      </nav>
    </header>
  );
};

export { Navigation };
