beforeEach('visit homepage', () => {
    // documentation implies this isn't necessary but I needed this explicit call
    // I assume these hooks get fired before the local storage is cleared by cypress
    cy.clearLocalStorage();
    cy.visit('/').get('#arad-codeLink').should('be.visible');
});
