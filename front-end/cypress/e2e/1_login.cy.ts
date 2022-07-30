import "../support/commands";
import { randomEmail } from "../support/utils";

describe("login", () => {
  it("succeeds", () => {
    const email = randomEmail();
    const passphrase = "passphrase";

    cy.register(email, passphrase)
      .logout()
      .login(email, passphrase)
      .get("#arad-logoutLink")
      .should("be.visible")
      .refreshToken()
      .should("be.not.empty")
      .pathShouldNotEqual("/login");
  });

  it("fails with incorrect passphrase", () => {
    const email = randomEmail();
    const passphrase = "passphrase";
    const incorrect_passphrase = "passphr4se";

    cy.register(email, passphrase)
      .logout()
      .login(email, incorrect_passphrase)
      .get("#login-errorMessage")
      .contains("incorrect username or password")
      .refreshToken()
      .should("be.empty")
      .pathShouldEqual("/login");
  });

  it("redirects when logged in", () => {
    const email = randomEmail();
    const passphrase = "passphrase";

    cy.register(email, passphrase)
      .get("#arad-logoutLink")
      .should("be.visible")
      .visit("/login")
      .pathShouldNotEqual("/login");
  });
});
