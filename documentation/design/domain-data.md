[arad](../../../../) / [documentation](../) / [design](./)

# Domain and Data Model

Domain and data modelling allow us to understand the problem space from different perspectives. The goal here is to
create two models that can interact to provide the correct application experience.

The domain model describes data entities from the domain perspective, uses real-world language for clarity, and
represents a template of the application state in memory at any given time. The domain model entities live in the
internal service layer of a service.

The data model describes data entities from the infrastructure perspective, and may use domain agnostic terms, at times,
for clarity. The data model represents a template of the application state on disk at any given time. The data model
entities live in the repository layer, and are defined in the model layer.

By decoupling these models through a repository layer abstraction, we are free to choose an entirely different
implementation for the data model (this is sometimes required for performance or cost reasons as scale increases),
or even an entirely different underling infrastructure. The service layer interface will not change in this case, and
application/endpoint code that calls it will not need modification.

## Domain Model

Arad is a simple distributed application. There are four service layers, all backed by the same underlying
infrastructure, sharing the same domain model.

### User

An Arad `User` is a domain entity that consumes resources from the Arad backend api. Most likely, `Users` will interface
through the provided `front-end` UX, but this is not a hard requirement.

#### Attributes

- id: UUID
- email: EmailAddress
- roles: Role[]

### Role

An Arad `Role` domain entity is an enumeration, and represents one of three possible values.

#### Possible Values:

- READER
- REVIEWER
- ADMINISTRATOR

### Article

- id: UUID
- doi: string
- title: string
- author: string
- ...
- duration: float
- difficulty: float
- jargon: string[]
- tags: string[]

### Review

- id: UUID
- article_id: UUID
- user_id: UUID
- duration: int
- difficulty: int
- jargon: string[]

## Data Model

### User

### Role

### UserRole


