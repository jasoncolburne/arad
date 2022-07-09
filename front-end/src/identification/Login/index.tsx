import { Role } from "../../datatypes/Role";
import { User } from "../../datatypes/User";
import { useGlobalState } from "../../GlobalState";

const admin: User = {
  roles: [Role.Administrator, Role.Reviewer],
  email: 'admin@arad.org',
};

const reviewer: User = {
  roles: [Role.Reviewer],
  email: 'reviewer@arad.org',
};

const Login = () => {
  const { state, setState } = useGlobalState();
  const loggedIn = state.user ? state.user.roles.length > 0 : false;

  if (!loggedIn) {
    const newState = { ...state, user: admin };
    setState(newState);
  }

  return (
    <div className="Login">
      <p>
        Login
      </p>
    </div>
  );
}

export { Login };
