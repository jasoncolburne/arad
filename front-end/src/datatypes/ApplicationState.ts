import { User, Role } from '../api/types/friendly';
import { Credentials, emptyCredentials } from './Credentials';

interface ApplicationState {
  credentials: Credentials;
  user: User;
  roles: Role[];
};

const emptyState: ApplicationState = {
  credentials: emptyCredentials,
  user: {
    id: '',
    email: '',
  },
  roles: [],
}

export type { ApplicationState };
export { emptyState };
