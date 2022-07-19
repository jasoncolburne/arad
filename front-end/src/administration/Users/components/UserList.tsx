import { Table, Tbody, Td, Th, Tr } from '@chakra-ui/react';
import { Role, User } from '../../../api/types/friendly';

import { UserListRow } from "./UserListRow";

interface UserListProps {
    users: User[];
    roles: Role[];
};

const UserList = (props: UserListProps) => {
    const { users, roles } = props;

    return (
        <Table>
            <Tbody>
                <Tr>
                    <Td>email</Td>
                    {roles.map((role) => {
                        return <Td>{role}</Td>;
                    })}
                </Tr>
                {users.map((user, index) => {
                    return <UserListRow index={index} user={user} roles={roles} />;
                })}
            </Tbody>
        </Table>
    )
};

export { UserList };