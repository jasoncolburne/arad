interface Credentials {
  refresh_token: string;
  access_tokens: {
    reader: string;
    reviewer: string;
    administrator: string;
  };
}

const emptyCredentials: Credentials = {
  refresh_token: "",
  access_tokens: {
    reader: "",
    reviewer: "",
    administrator: "",
  },
};

export type { Credentials };
export { emptyCredentials };
