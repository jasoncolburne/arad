import { User } from "../api/types/friendly";
import { Credentials, emptyCredentials } from "./Credentials";

interface ApplicationState {
  credentials: Credentials;
  user: User;
  query: string;
}

const emptyState: ApplicationState = {
  credentials: emptyCredentials,
  user: {
    id: "",
    email: "",
    roles: [],
  },
  query: ""
};

export type { ApplicationState };
export { emptyState };
