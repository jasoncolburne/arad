import { Checkbox, Td, Tr } from "@chakra-ui/react";
import { Api } from "../../../api/Api";
import { Role, RoleActions, RoleRequest, Roles, User } from "../../../api/types/friendly";
import { removeAccessTokenFromState, useGlobalState } from "../../../GlobalState";

interface UserListRowProps {
    user: User;
    roles: Role[];
}

const UserListRow = (props: UserListRowProps) => {
    const { user, roles } = props;
    const { state, setState } = useGlobalState();

    const handleErrors = (response: Response) => {
        if ([401, 403].includes(response.status)) {
          const newState = removeAccessTokenFromState(state, Roles.Administrator);
          setState(newState);
          // TODO: display errors
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
        }

        await Api().put('identify/role', state.credentials!.access_tokens.administrator, request, handleErrors);
    };

    return (
        <Tr>
            <Td>{user.email}</Td>
            {roles.map((role) => {
                const assigned = user.roles!.includes(role);

                return (
                    <Td>
                        <Checkbox
                            key={user.id + '-' + role}
                            colorScheme='gray'
                            size='lg'
                            defaultChecked={assigned}
                            onChange={(event) => { handleChange(event.target.checked, role) }}
                        />
                    </Td>
                );
            })}
        </Tr>
    );
};

export { UserListRow };