import React from "react";
import { Link } from "react-router-dom";

import { useGlobalState } from "../../../GlobalState";
import { isAdministrator } from "../../../utility/authorization";

import SearchBar from "./SearchBar";

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
        <SearchBar />
        {state.user !== undefined && isAdministrator(state.user.roles)
          ? adminLinks
          : null}
      </nav>
    </header>
  );
};

export { Navigation };
