import React, { FC } from "react";

import { Article } from "../../mock-data-util/mock-interface";

const ArticlesList: FC<{ results?: Article[] }> = ({
  results = [],
}): JSX.Element => {
  return (
    <>
      {Array.isArray(results) && results.length ? (
        results.map((article) => (

          <li key={article._id}>
            <h3>{article.title}</h3>
            <p>{article.content.substring(0, 100)} ...</p>
            <div className="user-rating">
              <p>USER RATING:</p>
              <p>{article.rating}</p>
            </div>
          </li>

        ))
      ) : (
        <h1>Search</h1>
      )}
    </>
  );
};

export default ArticlesList;
