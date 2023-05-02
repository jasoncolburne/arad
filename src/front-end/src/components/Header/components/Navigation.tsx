import React from "react";
import { Link } from "react-router-dom";

import { useGlobalState } from "../../../GlobalState";
import { isAdministrator } from "../../../utility/authorization";

// import SearchBar from "../../../core/Search/SearchBar";

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
        {/* <SearchBar /> */}
        {state.user !== undefined && isAdministrator(state.user.roles)
          ? adminLinks
          : null}
      </nav>
    </header>
  );
};

export { Navigation };
