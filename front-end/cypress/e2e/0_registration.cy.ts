import '../support/commands';
import { administratorCredentials, randomEmail } from '../support/utils';

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

    it('redirects when logged in', () => {
        const email = randomEmail();
        const passphrase = 'passphrase';

        cy.register(email, passphrase)
          .get('#arad-logoutLink').should('be.visible').visit('/register')
          .pathShouldNotEqual('/register');
    });

    it('for DEFAULT_ADMIN_EMAIL grants administrator privleges', () => {
        const { email, passphrase } = administratorCredentials;

        cy.register(email, passphrase)
          .get('#arad-usersLink').should('be.visible');
    });

    it('for user email, does not grant administrator privleges', () => {
      const email = randomEmail();
      const passphrase = 'passphrase';

      cy.register(email, passphrase)
        .get('#arad-usersLink').should('not.exist');
    });
});
