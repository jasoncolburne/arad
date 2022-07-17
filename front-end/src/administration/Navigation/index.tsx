import { Link } from "react-router-dom";

import { RoleEnum } from "../../api/types/friendly";
import { useGlobalState } from "../../GlobalState";

const adminLinks = (
  <>
    {" / "}<Link to="/articles">Manage Articles</Link>
    {" / "}<Link to="/users">Manage Users</Link>
  </>
);

const Navigation = () => {
  const { state } = useGlobalState();
  const isAdmin = state.roles!.includes(RoleEnum.Administrator) || false;

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
