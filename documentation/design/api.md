[arad](../../../../) / [documentation](../) / [design](./)

# The API Service

The API Layer is so simple, all it needs is an nginx config. In the future we must secure it with TLS.

There is no complicated mapping or translation in the api layer of the application (the API service). Instead, an
nginx proxy parses path prefixes to know what service to direct requests to - and the client application is aware of
the available endpoints on each path/service. We can apply authorization in the service itself and have far more control
over when we take certain backend actions - using [JWTs](./README.md#authentication-in-the-service-layer) to identify
the user making requests.
