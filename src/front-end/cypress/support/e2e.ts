beforeEach("visit homepage", () => {
  cy.visit("/").get("#arad-codeLink").should("be.visible");
});
