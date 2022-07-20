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
- email: string
- roles: Role[]

### Role

An Arad `Role` domain entity is an enumeration, and represents one of three possible values.

#### Possible Values:

- READER
- REVIEWER
- ADMINISTRATOR

### Article

An Arad `Article` is a domain entity that represents a real world research article. It is referenced by DOI (Digital
Object Identifier - [more details](https://en.wikipedia.org/wiki/Digital_object_identifier)).

#### Attributes

- id: UUID
- doi: string
- title: string
- author: string
- journal: string
- year: string
- volume: string | null
- pages: string | null
- duration: float
- difficulty: float
- jargon: string[]
- tags: string[]

### Review

An Arad `Review` is a domain entity that represents a review created in the system by a reviewer. A reviewer may review
an article at most once.

#### Attributes

- id: UUID
- article_id: UUID
- user_id: UUID
- duration: int
- difficulty: int
- comment: string
- jargon: string[]

## Data Model

The data model is composed of entities that represent abstract concepts and concerns related to the real world objects
in the domain model. In this case, our data model is best described by the database schema used in our underlying
relational database.

### User

#### Fields

- id: UUID
- email: email [indexed]
- hashed_passphrase: string

### Role

#### Fields

- id: UUID
- name: string [indexed]

### UserRole

#### Fields

- id: UUID
- user_id: UUID [indexed]
- role_id: UUID

#### Constraints

- foreign_key(user_id, User.id)
- foreign_key(role_id, Role.id)
- unique(user_id, role_id)

### Article

#### Fields

- id: UUID
- doi: string [indexed]
- title: string [indexed]
- author: string [indexed]
- journal: string [indexed]
- year: string [indexed]
- volume: string [nullable]
- pages: string [nullable]

#### Constraints

- unique(doi)

### Jargon

#### Fields

- id: UUID
- article_id: UUID [indexed]
- term: string [indexed]

#### Constraints

- foreign_key(article_id, Article.id)
- unique(article_id, term)

### Tag

#### Fields

- id: UUID
- name: string [indexed]

#### Constraints

- unique(name)

### ArticleTag

#### Fields

- id: UUID
- article_id: UUID [indexed]
- tag_id: UUID [indexed]

#### Constraints

- foreign_key(article_id, Article.id)
- foreign_key(tag_id, Tag.id)
- unique(atricle_id, tag_id)