# Setup

## Pre-requisites
- bash
- docker

## Setup
```
./sync
./local build
./database create
./database migrate
```

## Running
```
./local up
```

With your docker-compose services running, try navigating to `http://localhost`. We'll turn TLS 1.3 on before moving to
production.

You can edit any code, front-end or back-end, and it should live-update. Just remember to sync if you edit something in
`be-common`.

These steps are confirmed to work on MacOS Monterey/Intel and Ubuntu 20.04.4/WSL2 on Windows 10. Please reach out if
you run into problems so that we can update this page with requirements and steps for other systems.
