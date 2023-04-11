import React from "react";
import { Box, Center } from "@chakra-ui/layout";
import { useNavigate } from "react-router-dom";

import { Api } from "../../api/Api";
import {
  Role,
  Roles,
  RolesResponse,
  TokenRequest,
  TokenResponse,
  // User,
  UsersRequest,
  UsersResponse,
} from "../../api/types/friendly";
import { emptyState } from "../../datatypes/ApplicationState";
import { useGlobalState, modifyAccessToken } from "../../GlobalState";
import {
  isAdministrator,
  jwtValid,
  loggedIn,
} from "../../utility/authorization";
import { UserList } from "./components/UserList";
import { Spinner } from "@chakra-ui/react";

import mockUsers from "../../mock-data-util/mock-users.json";
import { MockUser } from "../../mock-data-util/mock-interface";

const Users = () => {
  const { state, setState } = useGlobalState();
  //                                    ** User
  const [users, setUsers] = React.useState<MockUser[]>(mockUsers);
  const [roles, setRoles] = React.useState<Role[]>([]);
  const [errorMessage, setErrorMessage] = React.useState("");
  const [page, setPage] = React.useState(1);
  const [totalPages, setTotalPages] = React.useState(1);
  const [filterText, setFilterText] = React.useState("");
  const [fetchingAccessToken, setFetchingAccessToken] = React.useState(false);
  const [fetchingRoles, setFetchingRoles] = React.useState(false);
  const [fetchingUsers, setFetchingUsers] = React.useState(false);
  const [rolesFetched, setRolesFetched] = React.useState(false);
  const [usersFetched, setUsersFetched] = React.useState(false);
  const navigate = useNavigate();

  const authorized =
    loggedIn(state.credentials!) && isAdministrator(state.user!.roles);
  const accessTokenValid =
    authorized && jwtValid(state.credentials!.access_tokens.administrator);

  React.useEffect(() => {
    const handleAccessErrors = (response: Response) => {
      if (response.status === 401) {
        setState(emptyState);
        navigate("/login");
      } else {
        setErrorMessage("something went wrong");
      }
    };

    const fetchAccessToken = async (request: TokenRequest) => {
      const response: TokenResponse | undefined = await Api().post(
        "identify/token",
        null,
        request,
        handleAccessErrors
      );

      if (response !== undefined) {
        const newState = modifyAccessToken(
          state,
          Roles.Administrator,
          response.access_token
        );
        setState(newState);
      }

      setFetchingAccessToken(false);
    };

    if (authorized && !accessTokenValid && !fetchingAccessToken) {
      const request: TokenRequest = {
        refresh_token: state.credentials!.refresh_token,
        scope: Roles.Administrator,
      };
      setFetchingAccessToken(true);
      fetchAccessToken(request);
    }
    // eslint-disable-next-line
  }, [authorized, accessTokenValid, fetchingAccessToken, setState, navigate]);

  React.useEffect(() => {
    const handleErrors = (response: Response) => {
      if (response.status === 401) {
        const newState = modifyAccessToken(state, Roles.Administrator, "");
        setState(newState);
        setErrorMessage("not authorized");
      } else {
        setErrorMessage("something went wrong");
      }
    };

    const fetchUsers = async (request: UsersRequest, accessToken: string) => {
      const response: UsersResponse | undefined = await Api().post(
        "identify/users",
        accessToken,
        request,
        handleErrors
      );

      if (response !== undefined) {
        setUsers(response.users); // ****
        setTotalPages(response.pages);
        setUsersFetched(true);

        if (rolesFetched) {
          setErrorMessage("");
        }
      }
      setFetchingUsers(false);
    };

    if (accessTokenValid && !fetchingUsers) {
      const request: UsersRequest = { email_filter: filterText, page };
      setUsersFetched(false);
      setFetchingUsers(true);
      fetchUsers(request, state.credentials!.access_tokens.administrator);
    }
    // eslint-disable-next-line
  }, [page, filterText, accessTokenValid, setState]);

  React.useEffect(() => {
    const handleErrors = (response: Response) => {
      if (response.status === 401) {
        const newState = modifyAccessToken(state, Roles.Administrator, "");
        setState(newState);
        setErrorMessage("not authorized");
      } else {
        setErrorMessage("something went wrong");
      }
    };

    const fetchRoles = async (access_token: string) => {
      const response: RolesResponse | undefined = await Api().get(
        "identify/roles",
        access_token,
        null,
        handleErrors
      );

      if (response !== undefined) {
        setRoles(response.roles);
        setRolesFetched(true);
        if (usersFetched) {
          setErrorMessage("");
        }
      }
      setFetchingRoles(false);
    };

    if (accessTokenValid && !rolesFetched && !fetchingRoles) {
      setFetchingRoles(true);
      fetchRoles(state.credentials!.access_tokens.administrator);
    }
    // eslint-disable-next-line
  }, [accessTokenValid, setState]);

  //  ! <-- remove ****                     ! <-- remove --> !
  if (authorized && errorMessage === "" && usersFetched && rolesFetched) {
    return (
      <Center>
        <Box w="container.xlg" h="100%">
          <UserList
            users={users}
            roles={roles}
            filterText={filterText}
            setFilterText={setFilterText}
            page={page}
            setPage={setPage}
            totalPages={totalPages}
          />
        </Box>
      </Center>
    );
  }
  if (authorized && errorMessage === "") {
    return (
      <Center h="100%">
        <Spinner id="users-loadingSpinner" />
      </Center>
    );
  } else {
    return (
      <Center id="users-errorMessage" h="100%">
        {errorMessage === "" ? "not authorized" : errorMessage}
      </Center>
    );
  }
};

export default Users;
