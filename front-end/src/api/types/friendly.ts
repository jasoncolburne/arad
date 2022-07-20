import { components as identify } from './identify';
import { components as administrate } from './administrate';

export type User = identify['schemas']['User'];
export type Role = identify['schemas']['Role'];

// this is fragile. if we ever update the roles in the back-end, we must adjust here
export enum Roles {
  Administrator = "ADMINISTRATOR",
  Reviewer = "REVIEWER",
  Reader = "READER"
};

export type LoginRequest = identify['schemas']['LoginRequest'];
export type LoginResponse = identify['schemas']['LoginResponse'];

export type RegisterRequest = identify['schemas']['RegisterRequest'];
export type RegisterResponse = identify['schemas']['RegisterResponse'];

export type TokenRequest = identify['schemas']['TokenRequest'];
export type TokenResponse = identify['schemas']['TokenResponse'];

export type RolesResponse = identify['schemas']['RolesResponse'];


export type UsersRequest = administrate['schemas']['UsersRequest'];
export type UsersResponse = administrate['schemas']['UsersResponse'];
