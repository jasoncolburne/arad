import { Center } from "@chakra-ui/layout";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Api } from "../../api/Api";
import { Roles, TokenRequest, TokenResponse, User, UsersRequest, UsersResponse } from "../../api/types/friendly";
import { ApplicationState, emptyState } from "../../datatypes/ApplicationState";
import { useGlobalState } from "../../GlobalState";
import { isAdministrator, jwtValid, loggedIn } from "../../utility/authorization";


const Users = () => {
  const { state, setState } = useGlobalState();
  const [users, setUsers] = useState<User[]>([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [page, setPage] = useState(1);
  const [fetchingAccessToken, setFetchingAccessToken] = useState(false);
  const navigate = useNavigate();

  const authorized = loggedIn(state.credentials!) && isAdministrator(state.roles!);
  const accessTokenValid = authorized && jwtValid(state.credentials!.access_tokens.administrator);


  const handleErrors = (response: Response) => {
    if ([401, 403].includes(response.status)) {
      const newState: ApplicationState = {
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
      setState(newState);
      setErrorMessage('not authorized');
    } else {
      setErrorMessage('something went wrong');
    }
  };

  const handleAccessErrors = (response: Response) => {
    if ([401, 403].includes(response.status)) {
      setState(emptyState);
      setFetchingAccessToken(false);
      navigate("/login");
    } else {
      setErrorMessage('something went wrong');
    }
  };

  useEffect(() => {
    const fetchAccessToken = async (request: TokenRequest) => {
      const response: TokenResponse = await Api().post('identify/token', null, request, handleAccessErrors);
      const newState: ApplicationState = {
        credentials: {
          refresh_token: state.credentials!.refresh_token,
          access_tokens: {
            reader: state.credentials!.access_tokens.reader,
            reviewer: state.credentials!.access_tokens.reviewer,
            administrator: response.access_token,
          },
        },
        user: state.user!,
        roles: state.roles!,
      };
      setState(newState);
      setFetchingAccessToken(false);
    }

    if (authorized && !accessTokenValid && !fetchingAccessToken) {
      const request: TokenRequest = { refresh_token: state.credentials!.refresh_token, scope: Roles.Administrator }
      setFetchingAccessToken(true);
      fetchAccessToken(request);
    }
  }, [
    authorized,
    accessTokenValid,
    fetchingAccessToken,
    state.credentials,
    state.user,
    state.roles,
    setState,
  ]);

  useEffect(() => {
    const fetchUsers = async (request: UsersRequest, access_token: string) => {
      const response: UsersResponse = await Api().post('administrate/users', access_token, request, handleErrors);
      setUsers(response.users);
      setErrorMessage('');
    };
  
    if (accessTokenValid) {
      const request: UsersRequest = { page };
      fetchUsers(request, state.credentials!.access_tokens.administrator);
    }
  }, [
    page,
    accessTokenValid,
    state.credentials,
  ]);

  if (authorized && errorMessage === '') {
      return (
      <Center h="100%">
        <div className="Users">
          <ul>
            {users.map((user, index) => { return <li key={index}>{user.email} ({user.id})</li>; })}
          </ul>
        </div>
      </Center>
    );
  } else {
    return (
      <Center h="100%">{errorMessage === '' ? 'unauthorized' : errorMessage}</Center>
    )
  }
}

export { Users };
