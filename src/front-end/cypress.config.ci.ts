import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: "http://front-end-nginx",
    specPattern: ["**/*.cy.ts"],
    video: false,
    screenshotOnRunFailure: false,
  },
});
