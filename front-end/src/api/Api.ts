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

      const url =
        currentHostname === "front-end"
          ? `http://api/api/v1/${endpoint}`
          : `http://${currentHostname}:81/api/v1/${endpoint}`;
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
