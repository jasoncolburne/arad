import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: "http://front-end",
    specPattern: ["**/*.cy.ts"],
  },
});
