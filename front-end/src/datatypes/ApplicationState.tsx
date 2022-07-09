import { Role } from "./Role";
import { User } from "./User";

interface ApplicationState {
  user: User;
  roles: Role[];
};

export type { ApplicationState };