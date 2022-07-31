[arad](../../../../) / [documentation](../README.md) / [development](./README.md)

# Setup

## Pre-requisites

- bash (get something like Debian on WSL2 if you're using Windows)
- docker

## Setup

The `nuke` command can be leveraged to setup your local environment.

```
arad $ scripts/local nuke
```

## Sanity Test

It's best to test that your local is setup correctly by running all test suites.

```
arad $ scripts/test e2e && scripts/test front-end && scripts/test back-end
```

## Running

```
arad $ scripts/local up
```

With your docker-compose services running, try navigating to `http://localhost`. We'll turn TLS 1.3 on before moving to
production. If you want to see the backend APIs, there is live documentation available at `http://localhost` on ports
`8000`-`8003` at `/docs`. Check out `http://localhost/8003/docs` to see the `identity` api documentation.

- `administrator` - `8000`
- `reviewer` - `8001`
- `reader` - `8002`
- `identity` - `8003`

You can edit any code, front-end or back-end, and it should live-update. Just remember to sync if you edit something in
`common`.

These steps are confirmed to work on MacOS Monterey/Intel and Ubuntu 20.04.4/WSL2 on Windows 10. Please reach out if
you run into problems so that we can update this page with requirements and steps for other systems.
