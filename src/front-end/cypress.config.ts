import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: "http://front-end-react",
    specPattern: ["**/*.cy.ts"],
  },
});
