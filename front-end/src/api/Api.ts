import { currentHostname } from "../Arad";

const Api = () => {
  const createHeaders = (token: String | null, body: Object | null) => {
    const result: HeadersInit = {};

    if (token) {
      result["Authorization"] = `Bearer ${token}`;
    }

    if (body) {
      result["Content-Type"] = "application/json";
    }

    return result;
  };

  const request = (method: string) => {
    const wrapper = async (
      endpoint: String,
      token: String | null,
      body: Object | null = null,
      handleErrors: Function
    ) => {
      const options: RequestInit = {
        method,
        headers: createHeaders(token, body),
      };

      if (body) {
        options.body = JSON.stringify(body);
      }

      const mapHostnameToHostname = (currentHostname: string): string => {
        return ["front-end-react", "front-end-nginx"].includes(currentHostname)
          ? "api"
          : currentHostname;
      };

      const mapHostnameToPort = (currentHostname: string): number => {
        if (["front-end-react", "front-end-nginx"].includes(currentHostname)) {
          return 80;
        }

        return currentHostname === "localhost" ? 8080 : 8443;
      };

      const mapHostnameToProtocol = (currentHostname: string): string => {
        return ["front-end-react", "front-end-nginx", "localhost"].includes(
          currentHostname
        )
          ? "http"
          : "https";
      };

      const hostname = mapHostnameToHostname(currentHostname);
      const port = mapHostnameToPort(currentHostname);
      const protocol = mapHostnameToProtocol(currentHostname);

      const url = `${protocol}://${hostname}:${port}/api/v1/${endpoint}`;

      const response = await fetch(url, options);

      if (!response.ok) {
        console.error(
          `error fetching ${endpoint}: ${response.status}, ${response.statusText}`
        );
        handleErrors(response);
        return undefined;
      }

      return await response.json();
    };

    return wrapper;
  };

  return {
    get: request("GET"),
    post: request("POST"),
    put: request("PUT"),
    delete: request("DELETE"),
  };
};

export { Api };
