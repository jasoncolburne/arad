import "../support/commands";
import { administratorCredentials, randomEmail } from "../support/utils";

describe("users", () => {
  it("cannot be accessed by a non-administrator user", () => {
    const email = randomEmail();
    const passphrase = "passphrase";

    cy.register(email, passphrase)
      .get("#arad-logoutLink").should("be.visible")
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
      .accessToken("ADMINISTRATOR").should("be.not.empty");
  });
});
