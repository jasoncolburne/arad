import { Input, Table, Tbody, Td, Tr } from '@chakra-ui/react';
import { Role, User } from '../../../api/types/friendly';

import { UserListRow } from "./UserListRow";

import { Paginator } from '../../../components/Paginator';
import { ChangeEvent, useState } from 'react';

interface UserListProps {
    users: User[];
    roles: Role[];
    setFilterText: Function;
    page: number;
    setPage: Function;
    totalPages: number;
};

const UserList = (props: UserListProps) => {
    const { users, roles, setFilterText, page, setPage, totalPages } = props;
    const [currentTimer, setCurrentTimer] = useState<NodeJS.Timeout | null>(null);

    const delayFilterChange = (event: ChangeEvent<HTMLInputElement>) => {
        if (currentTimer) {
            clearTimeout(currentTimer);
        }

        const timer = setTimeout(() => {
            setFilterText(event.target.value);
            setPage(1);
            setCurrentTimer(null);
        }, 666);

        setCurrentTimer(timer);
    }

    return (
        <Paginator page={page} totalPages={totalPages} setPage={setPage}>
            <Table>
                <Tbody>
                    <Tr>
                        <Td key='email-filter'>
                            <Input
                                borderRadius="lg"
                                focusBorderColor="black"
                                placeholder='email filter'
                                onChange={delayFilterChange}
                            />
                        </Td>
                        {roles.map((role) => {
                            return <Td key={role}>{role}</Td>;
                        })}
                    </Tr>
                    {users.map((user) => {
                        return <UserListRow key={user.id} user={user} roles={roles} />;
                    })}
                </Tbody>
            </Table>
        </Paginator>
    )
};

export { UserList };