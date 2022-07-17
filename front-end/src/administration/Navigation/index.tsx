import { Link } from "react-router-dom";

import { useGlobalState } from "../../GlobalState";
import { isAdministrator } from "../../utility/authorization";

const adminLinks = (
  <>
    {" / "}<Link to="/articles">Manage Articles</Link>
    {" / "}<Link to="/users">Manage Users</Link>
  </>
);

const Navigation = () => {
  const { state } = useGlobalState();

  return (
    <header>
      <nav>
        <Link to="/search">Search</Link>
        {isAdministrator(state.roles!) ? adminLinks : null}
      </nav>
    </header>
  );
}

export { Navigation };
