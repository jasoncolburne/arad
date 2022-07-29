import { Box, Center } from "@chakra-ui/layout";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Api } from "../../api/Api";
import { Role, Roles, RolesResponse, TokenRequest, TokenResponse, User, UsersRequest, UsersResponse } from "../../api/types/friendly";
import { emptyState } from "../../datatypes/ApplicationState";
import { useGlobalState, modifyAccessToken } from "../../GlobalState";
import { isAdministrator, jwtValid, loggedIn } from "../../utility/authorization";
import { UserList } from "./components/UserList";


const Users = () => {
  const { state, setState } = useGlobalState();
  const [users, setUsers] = useState<User[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [errorMessage, setErrorMessage] = useState('');
  // TODO: remove this disable once we are using pagination on the front end
  // eslint-disable-next-line
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filterText, setFilterText] = useState('');
  const [fetchingAccessToken, setFetchingAccessToken] = useState(false);
  const navigate = useNavigate();

  const authorized = loggedIn(state.credentials!) && isAdministrator(state.user!.roles);
  const accessTokenValid = authorized && jwtValid(state.credentials!.access_tokens.administrator);

  useEffect(() => {
    const handleAccessErrors = (response: Response) => {
      if ([401, 403].includes(response.status)) {
        setState(emptyState);
        setFetchingAccessToken(false);
        navigate("/login");
      } else {
        setErrorMessage('something went wrong');
      }
    };

    const fetchAccessToken = async (request: TokenRequest) => {
      const response: TokenResponse = await Api().post('identify/token', null, request, handleAccessErrors);
      const newState = modifyAccessToken(state, Roles.Administrator, response.access_token);
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
    state,
    setState,
    navigate,
  ]);

  useEffect(() => {
    const handleErrors = (response: Response) => {
      if ([401, 403].includes(response.status)) {
        const newState = modifyAccessToken(state, Roles.Administrator, '');
        setState(newState);
        setErrorMessage('not authorized');
      } else {
        setErrorMessage('something went wrong');
      }
    };

    const fetchUsers = async (request: UsersRequest, accessToken: string) => {
      const response: UsersResponse = await Api().post('identify/users', accessToken, request, handleErrors);
      setUsers(response.users);
      setTotalPages(response.pages);
      setErrorMessage('');
    };
  
    if (accessTokenValid) {
      const request: UsersRequest = { email_filter: filterText, page };
      fetchUsers(request, state.credentials!.access_tokens.administrator);
    }
  }, [
    page,
    filterText,
    accessTokenValid,
    state,
    setState,
  ]);

  useEffect(() => {
    const handleErrors = (response: Response) => {
      if ([401, 403].includes(response.status)) {
        const newState = modifyAccessToken(state, Roles.Administrator, '');
        setState(newState);
        setErrorMessage('not authorized');
      } else {
        setErrorMessage('something went wrong');
      }
    };

    const fetchRoles = async (access_token: string) => {
      const response: RolesResponse = await Api().get('identify/roles', access_token, null, handleErrors);
      setRoles(response.roles);
      // this can't be good, we're doing it twice in parallel, so the state of the variable will change
      // before we know that the other instance is ready
      setErrorMessage('');
    };
  
    if (accessTokenValid) {
      fetchRoles(state.credentials!.access_tokens.administrator);
    }
  }, [
    accessTokenValid,
    state,
    setState,
  ]);

  if (authorized && errorMessage === '') {
      return (
      <Center h="100%">
        <Box w="container.lg">
          <UserList
            users={users}
            roles={roles}
            setFilterText={setFilterText}
            page={page}
            setPage={setPage}
            totalPages={totalPages}
          />
        </Box>
      </Center>
    );
  } else {
    return (
      <Center h="100%">{errorMessage === '' ? 'unauthorized' : errorMessage}</Center>
    )
  }
}

export { Users };
