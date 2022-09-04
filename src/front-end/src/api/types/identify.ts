/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface paths {
  "/register": {
    post: operations["register_register_post"];
  };
  "/login": {
    post: operations["login_login_post"];
  };
  "/logout": {
    post: operations["logout_logout_post"];
  };
  "/token": {
    post: operations["access_token_token_post"];
  };
  "/roles": {
    get: operations["roles_roles_get"];
  };
  "/role": {
    put: operations["assign_role_role_put"];
  };
  "/users": {
    post: operations["users_users_post"];
  };
}

export interface components {
  schemas: {
    /** HTTPValidationError */
    HTTPValidationError: {
      /** Detail */
      detail?: components["schemas"]["ValidationError"][];
    };
    /** LoginRequest */
    LoginRequest: {
      /** Email */
      email: string;
      /** Passphrase */
      passphrase: string;
    };
    /** LoginResponse */
    LoginResponse: {
      /** Refresh Token */
      refresh_token: string;
      user: components["schemas"]["User"];
    };
    /** LogoutRequest */
    LogoutRequest: {
      /** Refresh Token */
      refresh_token: string;
    };
    /** LogoutResponse */
    LogoutResponse: {
      /** Status */
      status: string;
    };
    /** RegisterRequest */
    RegisterRequest: {
      /** Email */
      email: string;
      /** Passphrase */
      passphrase: string;
    };
    /** RegisterResponse */
    RegisterResponse: {
      /** Refresh Token */
      refresh_token: string;
      user: components["schemas"]["User"];
    };
    /**
     * Role
     * @description An enumeration.
     * @enum {undefined}
     */
    Role: "READER" | "REVIEWER" | "ADMINISTRATOR";
    /**
     * RoleAction
     * @description An enumeration.
     * @enum {undefined}
     */
    RoleAction: "ASSIGN" | "REVOKE";
    /** RoleRequest */
    RoleRequest: {
      /**
       * User Id
       * Format: uuid
       */
      user_id: string;
      role: components["schemas"]["Role"];
      action: components["schemas"]["RoleAction"];
    };
    /** RoleResponse */
    RoleResponse: {
      role: components["schemas"]["Role"];
    };
    /** RolesResponse */
    RolesResponse: {
      roles: components["schemas"]["Role"][];
    };
    /** TokenRequest */
    TokenRequest: {
      /** Refresh Token */
      refresh_token: string;
      scope: components["schemas"]["Role"];
    };
    /** TokenResponse */
    TokenResponse: {
      /** Access Token */
      access_token: string;
    };
    /** User */
    User: {
      /**
       * Id
       * Format: uuid
       */
      id: string;
      /** Email */
      email: string;
      roles: components["schemas"]["Role"][];
    };
    /** UsersRequest */
    UsersRequest: {
      /** Page */
      page?: number;
      /** Email Filter */
      email_filter: string;
    };
    /** UsersResponse */
    UsersResponse: {
      /** Users */
      users: components["schemas"]["User"][];
      /** Count */
      count: number;
      /** Page */
      page: number;
      /** Pages */
      pages: number;
    };
    /** ValidationError */
    ValidationError: {
      /** Location */
      loc: (Partial<string> & Partial<number>)[];
      /** Message */
      msg: string;
      /** Error Type */
      type: string;
    };
  };
}

export interface operations {
  register_register_post: {
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["RegisterResponse"];
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["RegisterRequest"];
      };
    };
  };
  login_login_post: {
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["LoginResponse"];
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["LoginRequest"];
      };
    };
  };
  logout_logout_post: {
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["LogoutResponse"];
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["LogoutRequest"];
      };
    };
  };
  access_token_token_post: {
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["TokenResponse"];
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["TokenRequest"];
      };
    };
  };
  roles_roles_get: {
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["RolesResponse"];
        };
      };
    };
  };
  assign_role_role_put: {
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["RoleResponse"];
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["RoleRequest"];
      };
    };
  };
  users_users_post: {
    responses: {
      /** Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["UsersResponse"];
        };
      };
      /** Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["UsersRequest"];
      };
    };
  };
}

export interface external {}