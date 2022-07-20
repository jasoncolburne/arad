import { useState, createContext, useContext, SetStateAction, Dispatch } from "react"
import { Role, Roles } from "./api/types/friendly";

import { ApplicationState } from "./datatypes/ApplicationState"

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
  const setState: Dispatch<SetStateAction<Partial<ApplicationState>>> = (new_state) => {
    localStorage.setItem('state', JSON.stringify(new_state));
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

const removeAccessTokenFromState = (state: Partial<ApplicationState>, scope: Role): ApplicationState => {
  if (scope === Roles.Administrator) {
    return {
      credentials: {
        refresh_token: state.credentials!.refresh_token,
        access_tokens: {
          reader: state.credentials!.access_tokens.reader,
          reviewer: state.credentials!.access_tokens.reviewer,
          administrator: '',
        },
      },
      user: state.user!,
      roles: state.roles!,
    };
  }

  if (scope === Roles.Reviewer) {
    return {
      credentials: {
        refresh_token: state.credentials!.refresh_token,
        access_tokens: {
          reader: state.credentials!.access_tokens.reader,
          reviewer: '',
          administrator: state.credentials!.access_tokens.administrator,
        },
      },
      user: state.user!,
      roles: state.roles!,
    };
  }

  return {
    credentials: state.credentials!,
    user: state.user!,
    roles: state.roles!,
  };
};

export { GlobalState, useGlobalState, removeAccessTokenFromState };
