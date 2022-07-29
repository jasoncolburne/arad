import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import { ColorModeScript } from "@chakra-ui/react";

import reportWebVitals from "./reportWebVitals";
import * as serviceWorker from "./serviceWorker";

import "./index.css";
import { Main } from "./main";

const App = () => {
  return (
    <>
      <ColorModeScript />
      <BrowserRouter>
        <Main />
      </BrowserRouter>
    </>
  );
};

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <App />
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://cra.link/PWA
serviceWorker.unregister();

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
