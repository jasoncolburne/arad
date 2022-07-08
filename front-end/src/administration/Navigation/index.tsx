import { Link } from "react-router-dom";

const Navigation = () => {
  return (
    <header>
      <nav>
        <Link to="/search">Search</Link>{" "}
        <Link to="/articles">Manage Articles</Link>{" "}
        <Link to="/users">Manage Users</Link>
      </nav>
    </header>
  );
}

export { Navigation };
