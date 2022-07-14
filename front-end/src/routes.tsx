import * as React from "react";
import { useEffect } from "react";
import { useLocation } from "react-router";
import { RouteObject, useNavigate } from "react-router-dom";
import { Article } from "./administration/Article";
import { User } from "./administration/User";
import { Analytics } from "./core/Analytics";
import { Request as PassphraseResetRequest } from "./identification/Passphrase/Reset/Request";
import { Confirm as PassphraseResetConfirm } from "./identification/Passphrase/Reset/Confirm";
import { Change as PassphraseChange } from "./identification/Passphrase/Change";
import { Register } from "./identification/Register";
import { Arad } from "./Arad";
import { Login } from "./identification/Login";
import { Redirect } from "./core/Redirect";

export enum RoutesEnum {
  HOME,
  REGISTER,
  LOGIN,
  PASSPHRASE,
  RESET,
  CONFIRM,
  SEARCH,
  ARTICLES,
  USERS,
  CODE,
}

const ROUTE_MAP: {
  [key in RoutesEnum]: RouteObject & {
    element: JSX.Element;
    isProtected?: boolean;
  };
} = {
  [RoutesEnum.HOME]: {
    path: "/",
    element: <Arad />,
  },
  [RoutesEnum.REGISTER]: {
    path: "register",
    element: <Register />,
  },
  [RoutesEnum.LOGIN]: {
    path: "login",
    element: <Login />,
  },
  [RoutesEnum.PASSPHRASE]: {
    path: "passphrase",
    element: <PassphraseChange />,
  },
  [RoutesEnum.RESET]: {
    path: "reset",
    element: <PassphraseResetRequest />,
  },
  [RoutesEnum.CONFIRM]: {
    path: "confirm",
    element: <PassphraseResetConfirm />,
  },
  [RoutesEnum.SEARCH]: {
    path: "search/:articleId",
    element: <Analytics />,
    isProtected: true,
  },
  [RoutesEnum.ARTICLES]: {
    path: "articles/:articleId",
    element: <Article />,
    isProtected: true,
  },
  [RoutesEnum.USERS]: {
    path: "users/:userId",
    element: <User />,
    isProtected: true,
  },
  [RoutesEnum.CODE]: {
    path: "code",
    element: <Redirect url="https://github.com/jasoncolburne/arad" />,
    isProtected: true,
  },
};

export const RequireAuth: React.FC<{ children: JSX.Element }> = ({
  children,
}) => {
  const navigate = useNavigate();
  const location = useLocation();
  useEffect(() => {
    // TODO: get the user object here...
    if (!user.isAuthenticated) {
      // save where they were going originally
      const query = new URLSearchParams();
      query.set("to", encodeURIComponent(location.pathname));
      // navigate to login with original query
      navigate(`/login?${query.toString()}`);
    }
  }, [location.pathname, navigate]);

  return children;
};

export const getPathByRoute = (route: RoutesEnum): string => {
  return ROUTE_MAP[route].path!;
};

const makeRoutes = (): RouteObject[] => {
  return Object.values(ROUTE_MAP).map((route) => ({
    path: route.path,
    element: route.isProtected ? (
      <RequireAuth>{route.element}</RequireAuth>
    ) : (
      route.element
    ),
  }));
};

export const routes = makeRoutes();
