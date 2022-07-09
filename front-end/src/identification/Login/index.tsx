import { useEffect } from "react";
import { Role } from "../../datatypes/Role";
import { User } from "../../datatypes/User";
import { useGlobalState } from "../../GlobalState";

const admin: User = {
  id: '1',
  email: 'admin@arad.org',
};

const roles: Role[] = [
  Role.Administrator,
  Role.Reviewer,
]

const Login = () => {
  const { state, setState } = useGlobalState();
  const loggedIn = state.roles!.length > 0;

  useEffect(() => {
    if (!loggedIn) {
      const newState = { ...state, user: admin, roles };
      setState(newState);
    }
  }, [loggedIn, setState, state]);

  return (
    <div className="Login">
      <p>
        Login
      </p>
    </div>
  );
}

export { Login };
