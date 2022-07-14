import { useRoutes } from "react-router-dom";

import { routes } from "./routes";

export const Main = () => {
  return useRoutes(routes);
};
