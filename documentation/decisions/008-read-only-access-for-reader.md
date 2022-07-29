[arad](../../../../) / [documentation](../README.md) / [decisions](./README.md)

# Read-Only Application Database Access for Reader Service

**Date**: 2022-07-29

**Decider(s)**: [@jasoncolburne](https://github.com/jasoncolburne)

**Status**: decided

The `reader` service does not need to write to the application database. Principle of least privilege states we should
thus restrict its access to read-only.


## Considered Options
- Read-Only Access
- Read/Write Access


## Decision Outcome

**Chosen Option**: Read-Only Access, to apply the principle of least privilege.
