import { components as identify } from './identify';
import { components as administrate } from './administrate';

export type Credentials = identify['schemas']['Credentials'];
export type User = identify['schemas']['User'];
export type Role = identify['schemas']['Role'];
export enum RoleEnum {
  Administrator = "ADMINISTRATOR",
  Reviewer = "REVIEWER",
  Reader = "READER"
};

export type LoginRequest = identify['schemas']['LoginRequest'];
export type LoginResponse = identify['schemas']['LoginResponse'];

export type RegisterRequest = identify['schemas']['RegisterRequest'];
export type RegisterResponse = identify['schemas']['RegisterResponse'];

export type UsersRequest = administrate['schemas']['UsersRequest'];
export type UsersResponse = administrate['schemas']['UsersResponse'];
