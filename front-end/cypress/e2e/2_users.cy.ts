import "../support/commands";
import { administratorCredentials, randomEmail } from "../support/utils";

describe("users", () => {
  it("cannot be accessed by a non-administrator user", () => {
    const email = randomEmail();
    const passphrase = "passphrase";

    cy.register(email, passphrase)
      .shouldBeLoggedIn(email)
      .visit("/users")
      .get("#users-errorMessage").contains("not authorized")
      .accessToken("ADMINISTRATOR").should("be.empty");
  });

  it("can be accessed by an administrator user", () => {
    const { email, passphrase } = administratorCredentials;

    cy.login(email, passphrase)
      .intercept("**/api/v1/identify/token").as("token")
      .get("#arad-usersLink").should("be.visible").click()
      .wait("@token")
      .get("#users-loadingSpinner").should("not.exist")
      .accessToken("ADMINISTRATOR").should("not.be.empty");
  });

  it("allows modification of roles by administrator", () => {
    const { email, passphrase } = administratorCredentials;

    cy.login(email, passphrase)
      .shouldBeLoggedIn(email)
      .userId().then((userId) => {
        const toggleId = `#users-roleToggle-${userId}-REVIEWER`;
        cy.userRoles().should("not.include", "REVIEWER")
          .intercept("**/api/v1/identify/users").as("users")
          .get("#arad-usersLink").should("be.visible").click()
          .wait("@users")
          .get("#users-filter").should("be.visible").type("admin")
          .wait("@users")
          .intercept("**/api/v1/identify/role").as("role")
          .get(toggleId).check({ force: true })
          .wait("@role")
          .logout()
          .get("#arad-passphraseLink").should("not.exist")
          .login(email, passphrase)
          .shouldBeLoggedIn(email)
          .userRoles().should("include", "REVIEWER");
        });
  });
});
