import '../support/commands';
import { randomEmail } from '../support/utils';

describe('registration', () => {
    it('succeeds', () => {
        const email = randomEmail();
        const passphrase = 'passphrase';

        cy.register(email, passphrase)
          .pathShouldNotEqual('/register')
    });

    it('fails if verification does not match passphrase', () => {
        const email = randomEmail();
        const passphrase = 'passphrase';
        const verification = 'passphr4se';

        cy.register(email, passphrase, verification)
          .pathShouldEqual('/register');
    });

    it('redirects to root when logged in', () => {
        const email = randomEmail();
        const passphrase = 'passphrase';

        cy.register(email, passphrase)
          .get('#arad-logoutLink').should('be.visible').visit('/register')
          .pathShouldNotEqual('/register');
    });
});