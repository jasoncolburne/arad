import { useState, createContext, useContext, SetStateAction, Dispatch } from "react"

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

export { GlobalState, useGlobalState };
