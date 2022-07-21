[arad](../../../../) / [documentation](../) / [design](./)

# The Anatomy of an Arad Production Deployment


## Software

This is the main component. It is scalable and secure by [design](../design/). The software is intended to be licensed
permissively and written in a clear and accessible way. It should serve as a template for anyone to learn concepts
required to develop software at scale, and the compromises made in this design due to problem constraints will be
identified clearly to provide direction to those with differing requirements on how to modify the design.

## Tooling

This is supporting software that helps developers write and deploy the primary software. It is critical to provide a
good developer experience to reduce overall cost of modifications.

## Infrastructure (and Staging)

This is an ongoing expense and requires integration with `Software`. In addition to the infrastructure required for a
production deployment, we must also have the ability to spin up a staging infrastructure stack for development. This
allows developers to test changes before deploying to production with more confidence that their modifications will work
correctly in the production environment.

### What's required?

- `PostgreSQL` database with `pgcrypto` extension installed for application data (volume will be low for Arad)
- `Redis` memory cache for storing refresh tokens
- Email integration for password resets (postmark, mailgun, mailchimp etc)
- Hosting for Arad components (TBD)


## Observability Integrations

Observability tooling allows a production application to be monitored as it runs. Without it, the analogy is similar to
that of flying an airplane or driving an automobile blindfolded.

The term aggregation is used because the software runs multiple instances of a given service simultaneously to respond
to load, meaning that logs for a single service will be produced from many sources.

### Log Aggregation

Log aggregation is the most basic method used to gather intelligence of a running application. It is often unstructured
and detailed. This means that we typically don't get signal about a failing application from monitoring logs, but
instead use them as an invaluable tool during investigation.

- SumoLogic (or equivalent)

### Error Aggregation

Error aggregation provides a way to quickly examine a broken application, giving structured details and most often a
stack trace that allows developers to quickly pinpoint failing code.

- Sentry.io (or equivalent)

### Monitoring

Monitoring provides things like graphs and and telemetry for the running application, and can be integrated with
alerting solutions when monitors fail to meet certain conditions.

Something like (but maybe cheaper)
- Honeycomb.io
- Datadog

### Alerting

Alerting lets humans know that something is going wrong with the running application. Typically the monitoring solution
will integrate with the alerting solution to initiate human response.

Something like
- Pagerduty


## Documentation

### Decisions

Technical [decisions](../decisions/) are recorded for context and reference. As software grows and requires refit, it is
often difficult to understand why certain decisions were made. Sometimes these decisions should be superceded, and the
process allows for this.

### Developer

[Developer](../development/) documentation provides guides for common developer tasks and allows someone with moderate
experience to quickly get up to speed on the project and become productive.

### Design

[Design](../design/) documentation provides a higher level view of the software for developers and stakeholders to
use as a common frame of reference during feature design.

### Operation

[Operational](../operation/) documentation provides a guide for those running and monitoring the software, including:

- Installation
- Configuration
- Administration
- Incident Response

## Third Party Audits

In addition to the team working directly on the software and deployment plan, third parties will be engaged to audit
these design concerns:

- User Experience
- Security
- Production/Staging Deployment
