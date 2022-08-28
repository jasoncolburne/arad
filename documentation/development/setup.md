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
arad $ scripts/test all
```

## Running

```
arad $ scripts/local up
```

With your docker-compose services running, try navigating to [http://localhost](http://localhost).

Here are some other useful urls:

- [http://localhost:8443/api/v1/identify/docs](http://localhost:8443/api/v1/identify/docs)
- [http://localhost:8443/api/v1/administrate/docs](http://localhost:8443/api/v1/administrate/docs)
- [http://localhost:8443/api/v1/review/docs](http://localhost:8443/api/v1/review/docs)
- [http://localhost:8443/api/v1/read/docs](http://localhost:8443/api/v1/read/docs)

You can edit any code, front-end or back-end, and it should live-update. Just remember to sync if you edit something in
`core`.

These steps are confirmed to work on MacOS Monterey/Intel and Ubuntu 20.04.4/WSL2 on Windows 10. Please reach out if
you run into problems so that we can update this page with requirements and steps for other systems.
