/// <reference types="../cypress" />

const register = (email: string, passphrase: string, verification: string | null = null): Cypress.Chainable<JQuery<HTMLElement>> => {
  return cy.get('#arad-registerLink').should('be.visible').click()
           .get('#register-email').should('be.visible').type(email)
           .get('#register-passphrase').type(passphrase)
           .get('#register-verification').type(verification ? verification : passphrase)
           .type('{enter}');
};

const login = (email: string, passphrase: string): Cypress.Chainable<JQuery<HTMLElement>> => {
  return cy.get('#arad-loginLink').should('be.visible').click()
           .get('#login-email').should('be.visible').type(email)
           .get('#login-passphrase').type(passphrase)
           .type('{enter}');
};

const logout = (): Cypress.Chainable<JQuery<HTMLElement>> => {
  return cy.get('#arad-logoutLink').should('be.visible').click();
};

const pathShouldEqual = (path: string): Cypress.Chainable<string> => {
  return cy.location('pathname').should('equal', path);
};

const pathShouldNotEqual = (path: string): Cypress.Chainable<string> => {
  return cy.location('pathname').should('not.equal', path);
};

declare namespace Cypress {
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
  }
};

Cypress.Commands.addAll(
  {
    register,
    login,
    logout,

    pathShouldEqual,
    pathShouldNotEqual
  }
);
