import { useEffect, useState } from "react";

import { User } from "../../datatypes/User";

const Users = () => {
  const [users, setUsers] = useState<User[]>([]);

  const fetchUsers = async () => {
    const response = await fetch("http://localhost:81/administrate/users")
    const users = await response.json()
    setUsers(users)
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div className="Users">
      <ul>
        {users.map((user) => { return <li>{user.email}</li>; })}
      </ul>
    </div>
  );
}

export { Users };
