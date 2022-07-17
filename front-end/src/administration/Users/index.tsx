import { Center } from "@chakra-ui/layout";
import { useEffect, useState } from "react";

import { Api } from "../../api/Api";
import { RoleEnum, User, UsersRequest, UsersResponse } from "../../api/types/friendly";
import { useGlobalState } from "../../GlobalState";


const Users = () => {
  const { state } = useGlobalState();
  const [users, setUsers] = useState<User[]>([]);
  const [errorMessage, setErrorMessage] = useState('');
  const authorized = state.credentials!.token !== '' && state.roles!.includes(RoleEnum.Administrator);

  const handleErrors = (response: Response) => {
    if ([401, 403].includes(response.status)) {
      setErrorMessage('not authorized');
    } else {
      setErrorMessage('something went wrong');
    }
  };

  useEffect(() => {
    const fetchUsers = async () => {
      const payload: UsersRequest = { page: 1 };
      const response: UsersResponse = await Api().post('administrate/users', state.credentials!.token, payload, handleErrors);
      setUsers(response.users)
    };

    if (authorized) {
      fetchUsers();
    }
  }, [authorized, state.credentials]);

  if (authorized && errorMessage === '') {
      return (
      <Center h="100%">
        <div className="Users">
          <ul>
            {users.map((user, index) => { return <li key={index}>{user.id}: {user.email}</li>; })}
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
