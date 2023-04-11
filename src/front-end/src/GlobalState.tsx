import React, {
  useState,
  createContext,
  useContext,
  SetStateAction,
  Dispatch,
} from "react";
import { LoginResponse, Role, Roles } from "./api/types/friendly";

import { ApplicationState } from "./datatypes/ApplicationState";
import { emptyCredentials } from "./datatypes/Credentials";

const GlobalContext = createContext({
  state: {} as Partial<ApplicationState>,
  setState: {} as Dispatch<SetStateAction<Partial<ApplicationState>>>,
});
GlobalContext.displayName = "GlobalContext";

const GlobalState = ({
  children,
  value = {} as ApplicationState,
}: {
  children: React.ReactNode;
  value?: Partial<ApplicationState>;
}) => {
  const [state, setStateCore] = useState(value);
  const setState: Dispatch<SetStateAction<Partial<ApplicationState>>> = (
    new_state
  ) => {
    localStorage.setItem("state", JSON.stringify(new_state));
    setStateCore(new_state);
  };

  return (
    <GlobalContext.Provider value={{ state, setState }}>
      {children}
    </GlobalContext.Provider>
  );
};

const useGlobalState = () => {
  const context = useContext(GlobalContext);

  if (!context) {
    throw new Error("useGlobalState must be used within a GlobalState element");
  }

  return context;
};

const modifyAccessToken = (
  state: Partial<ApplicationState>,
  scope: Role,
  token_value: string
): ApplicationState => {
  if (scope === Roles.Administrator) {
    return {
      credentials: {
        refresh_token: state.credentials!.refresh_token,
        access_tokens: {
          reader: state.credentials!.access_tokens.reader,
          reviewer: state.credentials!.access_tokens.reviewer,
          administrator: token_value,
        },
      },
      user: state.user!,
      query: state.query!
    };
  }

  if (scope === Roles.Reviewer) {
    return {
      credentials: {
        refresh_token: state.credentials!.refresh_token,
        access_tokens: {
          reader: state.credentials!.access_tokens.reader,
          reviewer: token_value,
          administrator: state.credentials!.access_tokens.administrator,
        },
      },
      user: state.user!,
      query: state.query!
    };
  }

  return {
    credentials: state.credentials!,
    user: state.user!,
    query: state.query!
  };
};

// we are using LoginResponse as a type here and really we sometimes pass an identical RegisterResponse
// this isn't great and should be fixed
const stateFromAuthenticationResponseData = (
  response: LoginResponse
): ApplicationState => {
  return {
    credentials: {
      ...emptyCredentials,
      refresh_token: response.refresh_token,
    },
    user: response.user,
    query: ""
  };
};

export {
  GlobalState,
  useGlobalState,
  modifyAccessToken,
  stateFromAuthenticationResponseData,
};
