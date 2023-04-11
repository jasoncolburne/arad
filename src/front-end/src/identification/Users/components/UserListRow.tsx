import React from "react";

import { Checkbox, Td, Tr } from "@chakra-ui/react";
import { Api } from "../../../api/Api";
import {
  Role,
  RoleActions,
  RoleRequest,
  Roles,
  // User,
} from "../../../api/types/friendly";
import { modifyAccessToken, useGlobalState } from "../../../GlobalState";

import { MockUser } from "../../../mock-data-util/mock-interface";

interface UserListRowProps {
  // ** User
  user: MockUser;
  roles: Role[];
}

const UserListRow = (props: UserListRowProps) => {
  const { user, roles } = props;
  const { state, setState } = useGlobalState();

  const handleErrors = (response: Response) => {
    if ([401, 403].includes(response.status)) {
      const newState = modifyAccessToken(state, Roles.Administrator, "");
      setState(newState);
      // TODO: display errors I suppose
      //   setErrorMessage('not authorized');
    } else {
      //   setErrorMessage('something went wrong');
    }
  };

  // this isn't very reliable, but it will do for the admin use case
  const handleChange = async (assign: boolean, role: Role) => {
    const request: RoleRequest = {
      user_id: user.id,
      role: role,
      action: assign ? RoleActions.Assign : RoleActions.Revoke,
    };

    await Api().put(
      "identify/role",
      state.credentials!.access_tokens.administrator,
      request,
      handleErrors
    );
  };

  const emailKey = `users-email-${user.id}`;

  

  return (
    <Tr>
      <Td id={emailKey} key={emailKey}>
        {user.email}
      </Td>
      {roles.map((role) => {
        const assigned = user.roles!.includes(role);
        const toggleKey = `users-roleToggle-${user.id}-${role}`;

        return (
          <Td key={toggleKey}>
            <Checkbox
              id={toggleKey}
              colorScheme="gray"
              size="lg"
              defaultChecked={assigned}
              onChange={(event) => {
                handleChange(event.target.checked, role);
              }}
            />
          </Td>
        );
      })}
    </Tr>
  );
};

export { UserListRow };
