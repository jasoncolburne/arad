import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Outlet, Routes, Route } from "react-router-dom";

import { ColorModeScript } from "@chakra-ui/react";
import { Arad } from "./Arad";

import reportWebVitals from "./reportWebVitals";
import * as serviceWorker from "./serviceWorker";

import "./index.css";
import { Redirect } from "./core/Redirect";

// code splitting
const Login = React.lazy(() => import("./identification/Login"));
const Register = React.lazy(() => import("./identification/Register"));
const PassphraseResetRequest = React.lazy(
  () => import("./identification/Passphrase/Reset/Request")
);
const PassphraseResetConfirm = React.lazy(
  () => import("./identification/Passphrase/Reset/Confirm")
);
const PassphraseChange = React.lazy(
  () => import("./identification/Passphrase/Change")
);

const Users = React.lazy(() => import("./identification/Users"));
const Article = React.lazy(() => import("./administration/Article"));
const Articles = React.lazy(() => import("./administration/Articles"));

const Search = React.lazy(() => import("./core/Search"));
const Analytics = React.lazy(() => import("./core/Analytics"));

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <>
    <ColorModeScript />
    <BrowserRouter>
      <React.Suspense fallback={<div>loading...</div>}>
        <Routes>
          <Route path="/" element={<Arad />}>
            {/* <Route index element={<Search />} /> */}

            {/* authentication */}
            <Route path="register" element={<Register />} />
            <Route path="login" element={<Login />} />
            <Route path="passphrase" element={<Outlet />}>
              <Route index element={<PassphraseChange />} />
              <Route path="reset" element={<Outlet />}>
                <Route index element={<PassphraseResetRequest />} />
                <Route path="confirm" element={<PassphraseResetConfirm />} />
              </Route>
            </Route>

            {/* core functionality */}
            <Route path="search" element={<Outlet />}>
              <Route index element={<Search />} />
              <Route path=":articleId" element={<Analytics />} />
            </Route>

            {/* admin */}
            <Route path="articles" element={<Outlet />}>
              <Route index element={<Articles />} />
              <Route path=":articleId" element={<Article />} />
            </Route>
            <Route path="users" element={<Users />} />
          </Route>

          {/* links */}
          <Route
            path="/code"
            element={<Redirect url="https://github.com/jasoncolburne/arad" />}
          />
        </Routes>
      </React.Suspense>
    </BrowserRouter>
  </>
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://cra.link/PWA
serviceWorker.unregister();

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
