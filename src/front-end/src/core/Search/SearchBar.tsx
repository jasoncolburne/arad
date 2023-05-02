import React, { useState, useEffect, useCallback, useRef } from "react";
// import { Link, useLocation } from "react-router-dom";

import { useGlobalState } from "../../GlobalState";
import { debounce } from "debounce";

const SearchBar = () => {
  const { setState } = useGlobalState();
  const [value, setValue] = useState("");
  // const location = useLocation();
  const onSearchRef = useRef<(value: string) => void>(() => {});

  const onSearch = useCallback(
    (query: string) => {
      setState((prev) => ({ ...prev, query }));
    },
    [setState]
  );

  useEffect(() => {
    onSearchRef.current = debounce((val: string) => onSearch(val), 400);
  }, [onSearch]);

  useEffect(() => {
    onSearchRef.current(value);
  }, [value]);

  return (
    <>
      {/* {location.pathname !== "/search" ? (
        <Link to="/search">Search</Link>
      ) : ( */}
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
      {/* )} */}
    </>
  );
};

export default SearchBar;
