import { Role, Roles } from "../api/types/friendly";
import { ApplicationState } from "../datatypes/ApplicationState";


export const isAdministrator = (roles: Role[]) => roles.includes(Roles.Administrator);
export const isReviewer = (roles: Role[]) => roles.includes(Roles.Reviewer);
export const isReader = (roles: Role[]) => roles.includes(Roles.Reader);

// we know that our application state is complete, this is by design
export const loggedIn = (state: Partial<ApplicationState>) => {
    return (/* state.credentials!.refreshToken !== '' && */ state.roles!.length > 0);
}
