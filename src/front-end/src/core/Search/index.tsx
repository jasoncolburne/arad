import React from "react";
import { useState, useEffect } from "react";

import { useGlobalState } from "../../GlobalState";

import mockArticles from "../../mock-data-util/mock-articles.json";
import { Article } from "../../mock-data-util/mock-interface";
import { searchArray } from "../../helper/searchDatabase";

import ArticlesList from "./ArticlesList";

import "./index.css";

const Search = () => {
  const [searchResults, setSearchResults] = useState<Article[]>([]);
  const { state } = useGlobalState();
  
  useEffect(() => {
    const results = searchArray(mockArticles.results, state.query)
    setSearchResults(results)
  }, [state.query])

  return (
    <div className="Search">
      <ArticlesList results={searchResults}/>
    </div>
  );
};

export default Search;
