import React from "react";
import { Input, Table, Tbody, Td, Tr } from "@chakra-ui/react";

import { Role, User } from "../../../api/types/friendly";

import { UserListRow } from "./UserListRow";
import { Paginator } from "../../../components/Paginator";

interface UserListProps {
  users: User[];
  roles: Role[];
  filterText: string;
  setFilterText: Function;
  page: number;
  setPage: Function;
  totalPages: number;
}

const UserList = (props: UserListProps) => {
  const { users, roles, filterText, setFilterText, page, setPage, totalPages } =
    props;
  const [currentTimer, setCurrentTimer] = React.useState<NodeJS.Timeout | null>(
    null
  );

  const delayFilterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (currentTimer) {
      clearTimeout(currentTimer);
    }

    const timer = setTimeout(() => {
      setFilterText(event.target.value);
      setPage(1);
      setCurrentTimer(null);
    }, 666);

    setCurrentTimer(timer);
  };

  return (
    <Paginator page={page} totalPages={totalPages} setPage={setPage}>
      <Table id="users-list">
        <Tbody>
          <Tr>
            <Td key="email-filter">
              <Input
                autoFocus
                id="users-filter"
                borderRadius="lg"
                focusBorderColor="black"
                defaultValue={filterText}
                placeholder="email filter"
                onChange={delayFilterChange}
              />
            </Td>
            {roles.map((role) => {
              return <Td key={role}>{role}</Td>;
            })}
          </Tr>
          {users.map((user) => {
            const rowKey = `users-row-${user.id}`;
            return <UserListRow key={rowKey} user={user} roles={roles} />;
          })}
        </Tbody>
      </Table>
    </Paginator>
  );
};

export { UserList };
