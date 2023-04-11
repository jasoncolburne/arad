const currentHostname = window.location.hostname;

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
const apiUri = `${protocol}://${hostname}:${port}/api/v1`;

export { currentHostname, apiUri };
 