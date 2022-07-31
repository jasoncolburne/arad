/// <reference types="cypress" />

interface Credentials {
  refresh_token: string;
  access_tokens: {
    reader: string;
    reviewer: string;
    administrator: string;
  };
}

type Role = "READER" | "REVIEWER" | "ADMINISTRATOR";

interface User {
  id: string;
  email: string;
  roles: Role[];
}

interface ApplicationState {
  credentials: Credentials;
  user: User;
}

const emptyUser: User = {
  id: "",
  email: "",
  roles: [],
};

const emptyCredentials: Credentials = {
  refresh_token: "",
  access_tokens: {
    administrator: "",
    reviewer: "",
    reader: "",
  },
};

const emptyState: ApplicationState = {
  credentials: emptyCredentials,
  user: emptyUser,
};

const getState = (): ApplicationState => {
  const _state = localStorage.getItem("state");
  const state: ApplicationState =
    _state === null ? emptyState : JSON.parse(_state);
  return state;
};

const register = (
  email: string,
  passphrase: string,
  verification: string | null = null
): Cypress.Chainable<JQuery<HTMLElement>> => {
  return cy.get("#arad-registerLink").should("be.visible").click()
           .get("#register-email").should("be.visible").type(email)
           .get("#register-passphrase").type(passphrase)
           .get("#register-verification").type(verification ? verification : passphrase)
           .type("{enter}");
};

const login = (
  email: string,
  passphrase: string
): Cypress.Chainable<JQuery<HTMLElement>> => {
  return cy.get("#arad-loginLink").should("be.visible").click()
           .get("#login-email").should("be.visible").type(email)
           .get("#login-passphrase").type(passphrase)
           .type("{enter}");
};

const shouldBeLoggedIn = (email: string): Cypress.Chainable<JQuery<HTMLElement>> => {
  return cy.get("#arad-passphraseLink").contains(email);
};

const shouldBeLoggedOut = (): Cypress.Chainable<JQuery<HTMLElement>> => {
  return cy.get("#arad-passphraseLink").should("not.exist");
};

const logout = (): Cypress.Chainable<JQuery<HTMLElement>> => {
  return cy.get("#arad-logoutLink").should("be.visible").click();
};

const pathShouldEqual = (path: string): Cypress.Chainable<string> => {
  return cy.location("pathname").should("equal", path);
};

const pathShouldNotEqual = (path: string): Cypress.Chainable<string> => {
  return cy.location("pathname").should("not.equal", path);
};

const applicationState = (): Cypress.Chainable<ApplicationState> => {
  return cy.wrap(getState());
};

const refreshToken = (): Cypress.Chainable<string> => {
  return cy.applicationState().its("credentials.refresh_token");
};

const accessToken = (scope: Role): Cypress.Chainable<string> => {
  return cy
    .applicationState()
    .its(`credentials.access_tokens.${scope.toLowerCase()}`);
};

const userId = (): Cypress.Chainable<string> => {
  return cy.applicationState().its("user.id");
};

const userRoles = (): Cypress.Chainable<Role[]> => {
  return cy.applicationState().its("user.roles");
}

declare namespace Cypress {
  // eslint-disable-next-line
  interface Chainable<Subject> {
    /**
     * Register to use the application. Null `verification` will verify with `passphrase`.
     * @example
     * cy.register('address@domain.org', 'passphrase');
     */
    register: typeof register;
    /**
     * Log in to the application
     * @example
     * cy.login('address@domain.org', 'passphrase');
     */
    login: typeof login;
    /**
     * Log out of the application
     * @example
     * cy.logout();
     */
    logout: typeof logout;
    /**
     * Assert that the user identified by `email` is logged in
     * @example
     * cy.shouldBeLoggedIn(email);
     */
    shouldBeLoggedIn: typeof shouldBeLoggedIn;
    /**
     * Assert that the no user is logged in
     * @example
     * cy.shouldBeLoggedOut();
     */
     shouldBeLoggedOut: typeof shouldBeLoggedOut;

    /**
     * Ensure the path is as expected, equal to the given value
     * @example
     * cy.pathShouldEqual('/users');
     */
    pathShouldEqual: typeof pathShouldEqual;
    /**
     * Ensure the path is as expected, and not the given value
     * @example
     * cy.pathShouldNotEqual('/login');
     */
    pathShouldNotEqual: typeof pathShouldNotEqual;

    /**
     * The current application state, read from local storage
     * @example
     * cy.applicationState().its('user.email').should('equal', email);
     */
    applicationState: typeof applicationState;
    /**
     * The current refreshToken
     * @example
     * cy.refreshToken().should('not.be.empty');
     */
    refreshToken: typeof refreshToken;
    /**
     * A current access token
     * @example
     * cy.accessToken('ADMINISTRATOR').should('not.be.empty');
     */
    accessToken: typeof accessToken;
    /**
     * The current user's id
     * @example
     * cy.userId().should('not.be.empty');
     */
    userId: typeof userId;
    /**
     * The current user's roles
     * @example
     * cy.userRoles().should('include', 'ADMINISTRATOR');
     */
     userRoles: typeof userRoles;
  }
}

Cypress.Commands.addAll({
  register,
  login,
  logout,
  shouldBeLoggedIn,
  shouldBeLoggedOut,

  pathShouldEqual,
  pathShouldNotEqual,

  applicationState,
  refreshToken,
  accessToken,

  userId,
  userRoles
});
