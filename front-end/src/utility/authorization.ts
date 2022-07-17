import jwt_decode from "jwt-decode";

import { Role, Roles } from "../api/types/friendly";
import { ApplicationState } from "../datatypes/ApplicationState";

export const isAdministrator = (roles: Role[]) => roles.includes(Roles.Administrator);
export const isReviewer = (roles: Role[]) => roles.includes(Roles.Reviewer);
export const isReader = (roles: Role[]) => roles.includes(Roles.Reader);

// we know that our application state is complete, this is by design
export const loggedIn = (state: Partial<ApplicationState>) => {
    return (/* state.credentials!.refreshToken !== '' && */ state.roles!.length > 0);
}

interface Jwt {
    sub: string;
    exp: number;
};

export const jwtValid = (access_token: string) => {
    if (access_token === '') {
        return false;
    }

    const decoded_jwt = jwt_decode<Jwt>(access_token);
    const unixTime = Math.floor(Date.now() / 1000);

    if (decoded_jwt.exp < unixTime - 15) {
        return false;
    }

    return true;
}
