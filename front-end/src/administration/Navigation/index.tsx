import { Link } from "react-router-dom";

import { Role } from "../../datatypes/Role";
import { User } from "../../datatypes/User";

const adminLinks = (
  <>
    {" / "}<Link to="/articles">Manage Articles</Link>
    {" / "}<Link to="/users">Manage Users</Link>
  </>
);

const Navigation = () => {
  const user: User = {
    roles: [],
    email: '',
  };
  
  const isAdmin = user.roles.includes(Role.Administrator)

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
