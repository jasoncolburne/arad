import { Table, Tbody, Td, Tr } from '@chakra-ui/react';
import { Role, User } from '../../../api/types/friendly';

import { UserListRow } from "./UserListRow";

import { Paginator } from '../../../components/Paginator';

interface UserListProps {
    users: User[];
    roles: Role[];
    page: number;
    totalPages: number;
    setPage: Function;
};

const UserList = (props: UserListProps) => {
    const { users, roles, page, totalPages, setPage } = props;

    return (
        <Table>
            <Paginator page={page} total={totalPages} setPage={setPage}>
                <Tbody>
                    <Tr>
                        <Td>email</Td>
                        {roles.map((role) => {
                            return <Td>{role}</Td>;
                        })}
                    </Tr>
                    {users.map((user, index) => {
                        return <UserListRow user={user} roles={roles} />;
                    })}
                </Tbody>
            </Paginator>
        </Table>
    )
};

export { UserList };