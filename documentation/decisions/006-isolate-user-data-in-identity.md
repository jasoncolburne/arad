[arad](../../../../) / [documentation](../README.md) / [decisions](./README.md)

# Isolate User Data Access to Identity

**Date**: 2022-07-29

**Decider(s)**: [@jasoncolburne](https://github.com/jasoncolburne)

**Status**: decided

We must provide an accessible template for a distributed app. With this we must implement a security model that will
suffice for the general case.

## Considered Options
- Isolate User Data in Identity
- Store User Data in Application Database


## Decision Outcome

**Chosen Option**: Isolate User Data in Identity, to provide a better example.

**Positive Consequences**:
- User data is not accessible by arbitrary application services

**Negative Consequences**:
- Higher complexity
