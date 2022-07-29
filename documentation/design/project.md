[arad](../../../../) / [documentation](../README.md) / [design](./README.md)

# Project Design

The git repository is a monorepo that contains source for all components of the distributed Arad application. For this
small project, this should work quite well. It allows us to:

- Easily obtain all source
- Make changes to common code nearly instantly rather than publishing and distributing a package

And it does not remove the flexibility to break the repository apart in the future.

## Front-End (arad/front-end)

The front end is a React SPA. Here is `arad/front-end/`:

```
front-end
├── cypress
│   ├── e2e
│   │   ├── login.cy.ts
│   │   └── registration.cy.ts
│   ├── screenshots
│   ├── support
│   │   ├── commands.ts
│   │   ├── e2e.ts
│   │   └── utils.ts
│   └── videos
├── public
│   ├── favicon.ico
│   ├── index.html
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   └── robots.txt
├── src
│   ├── administration
│   │   ├── Article
│   │   │   └── index.tsx
│   │   ├── Articles
│   │   │   └── index.tsx
│   │   ├── Navigation
│   │   │   └── index.tsx
│   │   ├── User
│   │   │   └── index.tsx
│   │   └── Users
│   │       ├── components
│   │       │   ├── UserList.tsx
│   │       │   └── UserListRow.tsx
│   │       └── index.tsx
│   ├── api
│   │   ├── types
│   │   │   ├── administrate.ts
│   │   │   ├── friendly.ts
│   │   │   ├── identify.ts
│   │   │   ├── read.ts
│   │   │   └── review.ts
│   │   └── Api.ts
│   ├── components
│   │   ├── Footer
│   │   │   ├── index.css
│   │   │   └── index.tsx
│   │   ├── Header
│   │   │   ├── index.css
│   │   │   └── index.tsx
│   │   └── Paginator
│   │       ├── components
│   │       │   └── PaginationControl.tsx
│   │       └── index.tsx
│   ├── core
│   │   ├── Analytics
│   │   │   └── index.tsx
│   │   ├── Redirect
│   │   │   └── index.tsx
│   │   └── Search
│   │       └── index.tsx
│   ├── datatypes
│   │   ├── ApplicationState.ts
│   │   └── Credentials.ts
│   ├── identification
│   │   ├── Login
│   │   │   └── index.tsx
│   │   ├── Passphrase
│   │   │   ├── Change
│   │   │   │   └── index.tsx
│   │   │   └── Reset
│   │   │       ├── Confirm
│   │   │       │   └── index.tsx
│   │   │       └── Request
│   │   │           └── index.tsx
│   │   └── Register
│   │       └── index.tsx
│   ├── utility
│   │   └── authorization.ts
│   ├── Arad.css
│   ├── Arad.test.tsx
│   ├── Arad.tsx
│   ├── ColorModeSwitcher.tsx
│   ├── GlobalState.tsx
│   ├── index.css
│   ├── index.tsx
│   ├── react-app-env.d.ts
│   ├── reportWebVitals.ts
│   ├── serviceWorker.ts
│   ├── setupTests.ts
│   └── test-utils.tsx
├── Dockerfile
├── README.md
├── build_types
├── cypress.config.ci.ts
├── cypress.config.ts
├── package.json
├── tsconfig.json
└── yarn.lock
```

In `src/`,
- `api` contains our API abstraction as well as generated types for back-end requests/responses.
- `datatypes` contains non-api types. We may want to make an `api` directory in here for discoverability.
- `utility` contains application wide utility code (auth code, currently)
- `components` contains common components
- `administration` administration features (check `Users/` for a small example of a feature)
- `identification` identification features (login, registration, passphrase)
- `core` primary application features (search, analytics, redirect.. probably want to put redirect in `components`)

We use [cypress](https://docs.cypress.io) for end-to-end tests. 

## A typical service (like arad/identity)

Here is `arad/identity/`:

```
identity
├── common
│   ├── datatypes
│   │   ├── __init__.py
│   │   ├── domain.py
│   │   ├── exception.py
│   │   └── response.py
│   ├── services
│   │   ├── __init__.py
│   │   └── authorization.py
│   ├── __init__.py
│   ├── app.py
│   ├── main.py
│   └── repl.py
├── database
│   ├── migrations
│   │   ├── versions
│   │   │   ├── 402096afc5b9_user.py
│   │   │   ├── 4e162e80fbba_userrole.py
│   │   │   └── f8bfefd4b530_role.py
│   │   ├── README
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── __init__.py
│   └── models.py
├── identity
│   ├── datatypes
│   │   ├── __init__.py
│   │   ├── domain.py
│   │   ├── request.py
│   │   └── response.py
│   ├── repositories
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   ├── __init__.py
│   ├── app.py
│   ├── cache.py
│   ├── mixins.py
│   ├── orchestrations.py
│   └── repl.py
├── tests
│   ├── identity_tests
│   │   ├── orchestration_tests
│   │   │   ├── __init__.py
│   │   │   ├── test_access_token.py
│   │   │   ├── test_login.py
│   │   │   ├── test_logout.py
│   │   │   ├── test_modify_role_assignment.py
│   │   │   ├── test_register.py
│   │   │   ├── test_roles.py
│   │   │   └── test_users.py
│   │   ├── repository_tests
│   │   │   ├── __init__.py
│   │   │   ├── test_auth.py
│   │   │   └── test_user.py
│   │   ├── service_tests
│   │   │   ├── __init__.py
│   │   │   ├── test_auth.py
│   │   │   └── test_user.py
│   │   ├── __init__.py
│   │   ├── test_cache.py
│   │   └── test_mixins.py
│   ├── __init__.py
│   └── test_identity.py
├── Dockerfile
├── activate
├── alembic.ini
├── mypy.ini
├── poetry.lock
└── pyproject.toml
```

The identity specific code lives in `identity/identity`. `common` was synced from `core` using the `sync` script. The
identity service uses its own database, so the database directory is unique to identity. In the other services, the
`sync` script also copies the `database` directory from `core` since these services share a data model and database.

## Scripts

The reader is encouraged to look at the source code of these scripts. The mapping of commands is at the bottom of each
file.

For a better reference, check the [Development How To?](../development/howto.md) guide.

### Sync

```
arad $ scripts/sync
```

Pretty simple script that rsyncs some files and then surgically removes a small subset where not needed. This should be
re-evaluated to trim down the code moved to each service.

### Database

```
arad $ scripts/database create
arad $ scripts/database migrate
arad $ scripts/sync && ./database generate-migrations MigrationName
arad $ scripts/database drop
arad $ scripts/database nuke
```

The `database` script does as it is commanded.

### Local

```
arad $ scripts/local build
arad $ scripts/local up
arad $ scripts/local down
arad $ scripts/local types
arad $ scripts/local exec poetry add awesome-new-package
```

The `local` script does various useful things.
