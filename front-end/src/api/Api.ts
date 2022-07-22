const Api = () => {
  const createHeaders = (token: String | null, body: Object | null) => {
    const result: HeadersInit = {};

    if (token) {
      result['Authorization'] = `Bearer ${token}`;
    }

    if (body) {
      result['Content-Type'] = 'application/json';
    }

    return result;
  };

  const request = (method: string) => {
    const wrapper = async (endpoint: String, token: String | null, body: Object | null = null, handleErrors: Function) => {
      const options: RequestInit = {
        method,
        headers: createHeaders(token, body),
      };

      if (body) {
        options.body = JSON.stringify(body);
      }

      const response = await fetch(`http://localhost:81/api/v1/${endpoint}`, options);

      if (!response.ok) {
        handleErrors(response);
        throw new Error(`error fetching ${endpoint}: ${response.status}, ${response.statusText}`)
      }

      return await response.json()
    }

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