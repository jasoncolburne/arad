[arad](../../../../) / [documentation](../) / [development](./)

# Setup

## Pre-requisites
- bash
- docker

## Setup

The `nuke` command can be leveraged to setup your local environment.

```
./local nuke
```

## Running
```
./local up
```

With your docker-compose services running, try navigating to `http://localhost`. We'll turn TLS 1.3 on before moving to
production. If you want to see the backend APIs, there is live documentation available at `http://localhost` on ports
`8000`-`8003` at `/docs`. Check out `http://localhost/8003/docs` to see the `identity` api documentation.

- `administrator` - `8000`
- `reviewer` - `8001`
- `reader` - `8002`
- `identity` - `8003`

You can edit any code, front-end or back-end, and it should live-update. Just remember to sync if you edit something in
`be-common`.

These steps are confirmed to work on MacOS Monterey/Intel and Ubuntu 20.04.4/WSL2 on Windows 10. Please reach out if
you run into problems so that we can update this page with requirements and steps for other systems.
