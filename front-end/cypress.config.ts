import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://front-end:3000',
    specPattern: ["**/*.cy.ts"]
  }
});
