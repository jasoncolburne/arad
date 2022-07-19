import { Checkbox, Td, Tr } from "@chakra-ui/react";
import { Role, User } from "../../../api/types/friendly";

interface UserListRowProps {
    index: number;
    user: User;
    roles: Role[];
}

const UserListRow = (props: UserListRowProps) => {
    const { index, user, roles } = props;

    return (
        <Tr>
            <Td>{user.email}</Td>
            {roles.map((role) => {
                return <Td><Checkbox key={user.id + '-' + role} colorScheme='gray' size='lg' defaultChecked={user.roles!.includes(role)}/></Td>;
            })}
        </Tr>
    );
};

export { UserListRow };