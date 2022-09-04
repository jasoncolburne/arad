import { apiUri } from "../uris";

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

      console.error(window.location.hostname);
      const response = await fetch(`${apiUri}/${endpoint}`, options);

      if (!response.ok) {
        console.error(
          `error fetching ${endpoint}: ${response.status}, ${response.statusText}`
        );
        handleErrors(response);
        return undefined;  // this is used by the caller when the response is not actionable
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
