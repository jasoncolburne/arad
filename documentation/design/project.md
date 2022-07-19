[arad](../../../../) / [documentation](../) / [design](./)

# Project Design

The git repository is a monorepo that contains source for all components of the distributed Arad application. For this
small project, this should work quite well. It allows us to:

- Easily obtain all source
- Make changes to common code nearly instantly rather than publishing and distributing a package

And it does not remove the flexibility to break the repository apart in the future.

## Front-End (arad/front-end)

The front end is a React SPA. Here is `arad/front-end/src/`:

```
src
├── administration
│   ├── Article
│   │   └── index.tsx
│   ├── Articles
│   │   └── index.tsx
│   ├── Navigation
│   │   └── index.tsx
│   ├── User
│   │   └── index.tsx
│   └── Users
│       ├── components
│       │   ├── UserList.tsx
│       │   └── UserListRow.tsx
│       └── index.tsx
├── api
│   ├── types
│   │   ├── administrate.ts
│   │   ├── friendly.ts
│   │   ├── identify.ts
│   │   ├── read.ts
│   │   └── review.ts
│   └── Api.ts
├── components
│   ├── Footer
│   │   ├── index.css
│   │   └── index.tsx
│   └── Header
│       ├── index.css
│       └── index.tsx
├── core
│   ├── Analytics
│   │   └── index.tsx
│   ├── Redirect
│   │   └── index.tsx
│   └── Search
│       └── index.tsx
├── datatypes
│   ├── ApplicationState.ts
│   └── Credentials.ts
├── identification
│   ├── Login
│   │   └── index.tsx
│   ├── Passphrase
│   │   ├── Change
│   │   │   └── index.tsx
│   │   └── Reset
│   │       ├── Confirm
│   │       │   └── index.tsx
│   │       └── Request
│   │           └── index.tsx
│   └── Register
│       └── index.tsx
├── utility
│   └── authorization.ts
├── Arad.css
├── Arad.test.tsx
├── Arad.tsx
├── ColorModeSwitcher.tsx
├── GlobalState.tsx
├── index.css
├── index.tsx
├── react-app-env.d.ts
├── reportWebVitals.ts
├── serviceWorker.ts
├── setupTests.ts
└── test-utils.tsx
```

- `api` contains our API abstraction as well as generated types for back-end requests/responses.
- `datatypes` contains non-api types. We may want to make an `api` directory in here for discoverability.
- `utility` contains application wide utility code (auth code, currently)
- `components` contains common components
- `administration` administration features (check `Users/` for a small example of a feature)
- `identification` identification features (login, registration, passphrase)
- `core` primary application features (search, analytics, redirect.. probably want to put redirect in `components`)

## A typical service (like arad/be-identity)

All back-end services are prefixed with `be-`. The only directory with this prefix that isn't an operational service is
`be-common` which contains code common to all other back-end repositories.

Here is `arad/be-identity/`:

```
be-identity
├── common
│   ├── __init__.py
│   ├── app.py
│   ├── main.py
│   ├── repositories
│   │   ├── __init__.py
│   │   ├── role.py
│   │   └── user.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── role.py
│   │   └── user.py
│   └── types
│       ├── __init__.py
│       ├── exception.py
│       ├── request.py
│       └── response.py
├── database
│   ├── __init__.py
│   ├── migrations
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── 25625d3e8eea_userrole.py
│   │       ├── 402096afc5b9_user.py
│   │       └── f8bfefd4b530_role.py
│   └── models.py
├── identity
│   ├── __init__.py
│   ├── app.py
│   ├── cache.py
│   ├── services
│   │   ├── __init__.py
│   │   └── authentication.py
│   └── types
│       ├── __init__.py
│       ├── request.py
│       └── response.py
├── tests
├   ├── __init__.py
├   └── test_node_identity.py
├── Dockerfile
├── README.md
├── alembic.ini
├── poetry.lock
└── pyproject.toml
```

The identity specific code lives in `be-identity/identity`. `common` and `database` were both synced from `be-common`
using the `sync` script.

## Scripts

The reader is encouraged to look at the source code of these scripts. The mapping of commands is at the bottom of each
file.

### Sync

```
arad $ ./sync
```

Pretty simple script that rsyncs some files and then surgically removes a small subset where not needed. This should be
re-evaluated to trim down the code moved to each service.

### Database

```
arad $ ./database create
arad $ ./database migrate
arad $ ./sync && ./database generate-migrations MigrationName
arad $ ./database drop
```

The `database` script does as it is commanded.

### Local

```
arad $ ./local build
arad $ ./local up
arad $ ./local down
arad $ ./local types
arad $ ./local be-exec poetry add awesome-new-package
```

The `local` script does various useful things.
