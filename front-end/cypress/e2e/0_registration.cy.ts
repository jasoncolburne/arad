import "../support/commands";
import { administratorCredentials, randomEmail } from "../support/utils";

describe("registration", () => {
  it("succeeds", () => {
    const email = randomEmail();
    const passphrase = "passphrase";

    cy.register(email, passphrase)
      .shouldBeLoggedIn(email)
      .refreshToken().should("not.be.empty")
      .pathShouldNotEqual("/register");
  });

  it("fails if verification does not match passphrase", () => {
    const email = randomEmail();
    const passphrase = "passphrase";
    const verification = "passphr4se";

    cy.register(email, passphrase, verification)
      .get("#register-errorMessage").contains("passphrases must match")
      .refreshToken().should("be.empty")
      .pathShouldEqual("/register");
  });

  it("fails if email already registered", () => {
    const email = randomEmail();
    const passphrase = "passphrase";

    cy.register(email, passphrase)
      .logout()
      .register(email, passphrase)
      .get("#register-errorMessage").contains("email address unavailable")
      .refreshToken().should("be.empty")
      .pathShouldEqual("/register");
  });

  it("fails if email address not an email address", () => {
    const email = 'invalid_email_address';
    const passphrase = "passphrase";

    cy.register(email, passphrase)
      .get("#register-errorMessage").contains("email address unavailable")
      .refreshToken().should("be.empty")
      .pathShouldEqual("/register");
  });

  it("redirects when logged in", () => {
    const email = randomEmail();
    const passphrase = "passphrase";

    cy.register(email, passphrase)
      .shouldBeLoggedIn(email)
      .visit("/register")
      .pathShouldNotEqual("/register");
  });

  it("for DEFAULT_ADMIN_EMAIL, grants administrator privleges", () => {
    const { email, passphrase } = administratorCredentials;

    cy.register(email, passphrase)
      .shouldBeLoggedIn(email)
      .userRoles().should("include", "ADMINISTRATOR");
  });

  it("for user email, does not grant administrator privleges", () => {
    const email = randomEmail();
    const passphrase = "passphrase";

    cy.register(email, passphrase)
      .shouldBeLoggedIn(email)
      .userRoles().should("not.include", "ADMINISTRATOR");
});
});
