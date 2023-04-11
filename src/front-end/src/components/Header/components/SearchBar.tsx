import React, { useState, useEffect, useCallback } from "react";
import { Link, useLocation } from "react-router-dom";

import { useGlobalState } from "../../../GlobalState";
import { debounce } from "debounce";

const SearchBar = () => {
  const { setState } = useGlobalState();
  const [value, setValue] = useState("");
  const location = useLocation();

  const onSearch = useCallback(
    (query: string) => setState((prev) => ({ ...prev, query })),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const onSearchDelay = debounce((val: string) => onSearch(val), 400);

  useEffect(() => {
    onSearchDelay(value);
  }, [onSearchDelay, value]);

  return (
    <>
      {location.pathname !== "/search" ? (
        <Link to="/search">Search</Link>
      ) : (
        <section className="search">
          <form className="search-form" onSubmit={(e) => e.preventDefault()}>
            <input
              className="search-input"
              spellCheck="false"
              placeholder="search articles"
              name="search"
              type="text"
              value={value}
              onChange={(e) => setValue(e.target.value)}
            />
          </form>
        </section>
      )}
    </>
  );
};

export default SearchBar;
