beforeEach('visit homepage', () => {
    // documentation implies this isn't necessary but I needed this explicit call
    // I assume these hooks get fired before the local storage is cleared by cypress
    cy.clearLocalStorage();
    cy.intercept('**/api/v1/identify/login').as('login')
      .intercept('**/api/v1/identify/logout').as('logout')
      .intercept('**/api/v1/identify/register').as('register')
      .visit('/').get('#arad-codeLink').should('be.visible');
});
