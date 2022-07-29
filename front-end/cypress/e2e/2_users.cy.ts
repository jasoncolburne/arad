import '../support/commands';
import { administratorCredentials, randomEmail } from '../support/utils';

describe('users', () => {
    it('cannot be accessed by a non-administrator user', () => {
        const email = randomEmail();
        const passphrase = 'passphrase';

        cy.register(email, passphrase)
          .get('#arad-logoutLink').should('be.visible').visit('/users')
          .get('#users-filter').should('not.exist');
    });

    it('can be accessed by an administrator user', () => {
        const { email, passphrase } = administratorCredentials;

        cy.login(email, passphrase)
          .get('#arad-usersLink').should('be.visible').click()
          .get('#users-filter').should('be.visible');
    });
});
