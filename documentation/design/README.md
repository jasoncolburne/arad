[arad](../../../../)/[documentation](../)

# Design

- [Front-end Layer](#front-end-layer)
- [API Layer](#api-layer)
- [Service Layer](#service-layer)
    - [Identity](#identity)
    - [Reader](#reader)
    - [Reviewer](#reviewer)
    - [Administrator](#administrator)
- [Infrastructure Layer](#infrastructure-layer)
    - [Database](#database)
    - [Cache](#cache)

`Arad` is designed in layers. A layer recieves a request from above, does some processing and makes requests to the
layer below to compose a response to return to the layer above. By enforcing this architecture (easy enough in this
application) we can ensure our [distributed traces](https://en.wikipedia.org/wiki/Tracing_(software))
are short, understandable and debuggable.

Within services, we maintain a similar rigidity and layering where layers only interact up and down with adjacent
layers, in isolation from processes in their own layer. Thanks to A. Tucker for teaching me this technique.

By grouping functionality by user type/concern, we can scale components of the system independently, reacting to
changes in user behaviour.

![Arad](./assets/arad-simple.png)

## Front-end Layer
The top layer, the [`front-end`](https://en.wikipedia.org/wiki/Frontend_and_backend), is located in the `client`. The
client may take many forms. Some examples include web browsers, mobile phones, or a variety of
[headless](https://en.wikipedia.org/wiki/Headless_computer) clients.

The `front-end` is a [React](https://reactjs.org/) [Single Page Application](https://en.wikipedia.org/wiki/Single-page_application).

## API Layer
It commmunicates with the `back-end` stack (everything else) through an the internet, and ultimately, an interface
called `api` - ([Application Programming Interface](https://en.wikipedia.org/wiki/API)). The sole responsibility of
`api` is to proxy incoming requests to the appropriate `back-end` services. Navigating down the stack, `api` is the
second layer.

## Service Layer
`api` delegates responsibility for processing these requests to one of four `back-end` services. The four services
running in the backend compose the `service` layer of our software graph. The services do not use any form of
direct inter-service messaging, like synchronous [RPC](https://en.wikipedia.org/wiki/Remote_procedure_call).
Additionally, they do not use any sophistocated mechanisms to transfer data and state. Instead, all user and
application state is stored in a relational database and cached in a distributed memory store where appropriate. This
eliminates several operational problems and should work well for this read-heavy application.

### Identity
`identity` is the foundational piece of the service layer, providing authentication and authorization capabilities to
permit [RBAC](https://en.wikipedia.org/wiki/Role-based_access_control). As there is no interservice communication,
we rely on other mechanisms to authorize user actions.

#### Authentication
Two forms of authentication exist in identity. Short-lived and long-lived. Access is controlled by short-lived tokens
that are generated using a long-lived refresh token that is aquired through user authentication (password, sso, etc).

[Here](https://www.oauth.com/oauth2-servers/making-authenticated-requests/refreshing-an-access-token/) is an example of
such a scheme.

For example, one scenario requiring protection is the ability of an `Administrator` to list users. We cannot allow
`Reviewers` or `Readers` to manage or view other user accounts. To accomplish this, we will use a concept of `roles`
named `reader`, `reviewer`, and `administrator`. The roles are not exclusive. Each short-lived access token can be
assigned a `scope` that corresponds to a `role`. This permits modularity of composition when applying RBAC.

When an `Administrator` clicks `Manage Users`, for example, the `front-end` will:
1. Examine its local data store for a valid, short-lived, `administrator`-scoped token.
1. Depending on the result, it will use that token to access the resource, or the `front-end` will:
    1. Use or acquire a valid refresh token to procure a short-lived `administrator`-scoped access token from `identity`.
    1. Use the short-lived token to access the resource.

This kind of separation of concerns allows us to easily implement password auth when acquiring an `administrator` token,
but not when requiring a `reviewer` token. If we have need for higher security in the future, additional protocols can
be layered on as the system is extended.

From what I have seen, it looks like the signing mechanism in the typical JWT flow uses a symmetric key. This is bizarre
to me. I want to fix this, so that we can reduce our attack surface by storing the private portion of an asymmetric
keypair in `identity` and only public portions in all the other services. This is indicated by coloring in the diagram
above. This method of verifying authorization doesn't require database or cache reads, and it's possible to invalidate
all tokens instantly by updating the public keys in the non-`identity` services. In fact, the system could be built
with backup keys in place and a rollover switch so that there is very little downtime due to a desync between `identity`
and the other services.

#### Endpoints

- login
- logout
- passphrase_reset
- passphrase_change (request and confirm)
- token

### Reader

The `reader` service is where most of the run-time compute resources for Arad will be consumed. This service responds
to requests from everyone, both authenticated and unauthenticated. A `reader` role has been included in the RBAC model
for completeness but due to the nature of `Reader` access, it will be rarely used.

#### Endpoints

- analytics
- search

### Reviewer

The `reviewer` service will allow `Reviewers` to submit reviews about articles.

#### Endpoints

- review

### Administrator

The `administrator` service will allow `Administrators` to modify information about articles and users.

#### Endpoints

- articles
- articles/:article_id
- users
- users/:user_id

# Infrastructure Layer

The infrastructure is composed of the database, and a distributed memory cache (not pictured) to improve performance.

By having only a single hard dependency, we can be assured of a higher uptime/downtime ratio.

## Database

The most useful and understood database type in this scenario is likely a relational database, but we are evaluating
alternatives. The current developer stack relies on PostgreSQL.

## Cache

To allow higher performance we can cache some database objects in memory (particularly, things like refresh tokens).
