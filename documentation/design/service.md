[arad](../../../../) / [documentation](../)

# A typical Arad service node

Each `service` layer node is composed of multiple layers. The same rule applies here that applied to the distributed
architecture. We should only call _down_ deeper into the stack, never up or sideways. this prevents circular stack
traces and makes code easier to debug.

![Typical service stack](./assets/service-stack.png)

## Endpoint layer

The `endpoint` layer is responsible for orchestrating service calls. This is not typical, and normally we'd inject an
orchestration layer between the endpoints and services to decouple them and delegate responsibility of encoding and
decoding alone to the endpoint layer. In this case, however, we do not plan to produce features that will change the
requirements and force us to orchestrate the same actions in multiple scenarios - for example, we won't need another
api. It is also highly unlikely we'll ever need inter-service communication outside the storage layer (application
state) - JWT access tokens solve the need for queries during authorization and there is no other known case that
requires it (to be confirmed).

If the need _does_ arise, do not hesitate to add an orchestration layer to decouple services and endpoints.

Authorization also happens at the endpoint layer, using decoration.

## Service layer

The service layer is where the application/domain logic will live. This is the most critical internal layer in the
entire distributed application. It is responsible for the core functionality of Arad.

It sequences actions, from the application perspective. For example, the `identity` service will have an endpoint
named `login` that accepts some form of authentication, and to perform this authentication, the endpoint must call
deeper into the application to reach the code that interfaces with the database. To accomplish this, the endpoint layer
above will use one or more services to invoke the required code in steps. The service code really only has one
objective in this application, to make its way to the database. We'll wrap the model code in repositories even through
it is not entirely necessary as we are doubtful to migrate off the initial data store.

## Repository layer

The repository layer provides an abstraction over the models, which represent database table schemas. As stated above,
it probably isn't entirely necessary to decouple the database and service layer with this repository layer, but it
should future-proof us if we want to change the interface to the database.

## Common code and sync

In addition to all the services, there is a `common` service that is not invoked when the application runs, but instead
holds code common to all other services. While we could package this up in a library, and may in the future, a simple
sync script accelerates development.
