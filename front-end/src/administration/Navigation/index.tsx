import { Link } from "react-router-dom";

import { Role } from "../../datatypes/Role";
import { useGlobalState } from "../../GlobalState";

const adminLinks = (
  <>
    {" / "}<Link to="/articles">Manage Articles</Link>
    {" / "}<Link to="/users">Manage Users</Link>
  </>
);

const Navigation = () => {
  const { state } = useGlobalState();
  const isAdmin = state.user ? state.user.roles.includes(Role.Administrator) : false;

  return (
    <header>
      <nav>
        <Link to="/search">Search</Link>
        {isAdmin ? adminLinks : null}
      </nav>
    </header>
  );
}

export { Navigation };
