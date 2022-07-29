[arad](../../../../) / [documentation](../README.md) / [decisions](./README.md)

# Employ End to End Testing

**Date**: 2022-07-29

**Decider(s)**: [@jasoncolburne](https://github.com/jasoncolburne)

**Status**: decided

**User Story**: [#119](https://github.com/jasoncolburne/arad/issues/119)

We need a way to provide test coverage for user behaviours/flows. These tests, unlike unit tests, will not worry about
any internals of our system. They should rarely need to change, and should allow us to refactor aggressively should we
need to.


## Considered Options
- Behavioural (Service-level) Tests
- End-to-End Tests


## Decision Outcome

**Chosen Option**: End-to-End Tests, since they will ultimately cost less to maintain than behavioural tests and
provide better coverage.

## Pros and Cons of the Options

### Behavioural Tests
- Good, because they cover broader integrations
- Bad, because they cannot cover many user actions that are distributed across the eco-system and support of these use
cases will require significant effort
- Bad, because they are often slow to run

### End-to-End Tests
- Good, because they cover the broadest of integrations and encapsulate all user actions
- Bad, because they are often complex to set up
- Bad, because they are often slow to run
