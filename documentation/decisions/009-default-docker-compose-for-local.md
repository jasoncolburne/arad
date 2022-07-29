[arad](../../../../) / [documentation](../README.md) / [decisions](./README.md)

# Use `docker-compose.yml` for Local Development

**Date**: 2022-07-29

**Decider(s)**: [@jasoncolburne](https://github.com/jasoncolburne)

**Status**: decided

When developing, we often need to use `docker compose` commands.

There are three environments for which we have compose requirements - local development, production build and ci
testing.

We must choose which environment to optimize for, by naming that environment's compose file `docker-compose.yml` to
permit the omission of the -f parameter when invoking the `docker compose` command.


## Considered Options
- Default Compose for Local Development
- Default Compose for Production Build
- Default Compose for CI Test


## Decision Outcome

**Chosen Option**: Default Compose for Local Development. We run these commands routinely while developing locally, and
rarely (often only to debug) in other environments.
