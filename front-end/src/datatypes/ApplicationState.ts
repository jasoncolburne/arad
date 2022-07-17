import { User, Role, Credentials } from '../api/types/friendly';

interface ApplicationState {
  credentials: Credentials;
  user: User;
  roles: Role[];
};

const emptyState: ApplicationState = {
  credentials: {
    token: '',
    token_type: '',
  },
  user: {
    id: '',
    email: '',
  },
  roles: [],
}

export { emptyState };
export type { ApplicationState };