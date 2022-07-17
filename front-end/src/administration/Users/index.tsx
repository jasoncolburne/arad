import { Center } from "@chakra-ui/layout";
import { useEffect, useState } from "react";

import { Api } from "../../api/Api";
import { User, UsersRequest, UsersResponse } from "../../api/types/friendly";
import { useGlobalState } from "../../GlobalState";
import { isAdministrator } from "../../utility/authorization";


const Users = () => {
  const { state } = useGlobalState();
  const [users, setUsers] = useState<User[]>([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [page, setPage] = useState(1);
  const authorized = state.credentials!.token !== '' && isAdministrator(state.roles!);

  const handleErrors = (response: Response) => {
    if ([401, 403].includes(response.status)) {
      setErrorMessage('not authorized');
    } else {
      setErrorMessage('something went wrong');
    }
  };

  useEffect(() => {
    const fetchUsers = async () => {
      const request: UsersRequest = { page };
      const response: UsersResponse = await Api().post('administrate/users', state.credentials!.token, request, handleErrors);
      setUsers(response.users)
    };

    if (authorized) {
      fetchUsers();
    }
  }, [authorized, page, state.credentials]);

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
