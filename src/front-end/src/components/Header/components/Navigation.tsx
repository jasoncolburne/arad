import React from "react";
import { Link, useLocation } from "react-router-dom";

import { useGlobalState } from "../../../GlobalState";
import { isAdministrator } from "../../../utility/authorization";

import SearchBar from "../../../core/Search/SearchBar";


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
  const location = useLocation();

  return (
    <header>
      <nav>
        {location.pathname !== "/search" ? (
          <Link to="/search">Search</Link>
        ) : (
          <SearchBar />
        )}
        {state.user !== undefined && isAdministrator(state.user.roles)
          ? adminLinks
          : null}
      </nav>
    </header>
  );
};

export { Navigation };
