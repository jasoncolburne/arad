import { v4 as uuidv4 } from "uuid";

const randomEmail = (
  prefix: string = "user",
  domain: string = "domain.org"
) => {
  return `${prefix}+${uuidv4()}@${domain}`;
};

const administratorCredentials = {
  email: "admin@domain.org",
  passphrase: "admin_passphrase",
};

export { randomEmail, administratorCredentials };
