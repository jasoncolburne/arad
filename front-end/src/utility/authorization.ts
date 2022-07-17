import jwt_decode from "jwt-decode";

import { Role, Roles } from "../api/types/friendly";
import { Credentials } from "../datatypes/Credentials";

export const isAdministrator = (roles: Role[]) => roles.includes(Roles.Administrator);
export const isReviewer = (roles: Role[]) => roles.includes(Roles.Reviewer);
export const isReader = (roles: Role[]) => roles.includes(Roles.Reader);

// we know that our application state is complete, this is by design
export const loggedIn = (credentials: Credentials) => {
    return credentials.refresh_token !== '';
}

interface Jwt {
    sub: string;
    exp: number;
};

export const jwtValid = (accessToken: string) => {
    if (accessToken === '') {
        return false;
    }

    const decodedJWT = jwt_decode<Jwt>(accessToken);
    const unixTime = Math.floor(Date.now() / 1000);

    console.log(decodedJWT.exp - unixTime);

    if (decodedJWT.exp < unixTime - 15) {
        return false;
    }

    return true;
}
