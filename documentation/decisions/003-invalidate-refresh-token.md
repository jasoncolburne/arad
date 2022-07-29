[arad](../../../../) / [documentation](../README.md) / [decisions](./README.md)

# Provide Mechanism to Invalidate Refresh Token

**Date**: 2022-07-19

**Decider(s)**: [@jasoncolburne](https://github.com/jasoncolburne), [@Stampnerd](https://github.com/Stampnerd)

**Status**: decided

In the event of a known compromomised refresh token, we need a way to prevent a malicious actor from gaining access
to controlled resources.


## Considered Options
- Invalidate all refresh tokens
- Invalidate compromised token
- Invalidate no tokens


## Decision Outcome

**Chosen Option**:  Invalidate compromised token

**Positive Consequences**:
- Malicious actor denied access
- Other users stay logged in


## Pros and Cons of the Options

### Invalidate all refresh tokens
- Good, because malicious actor denied access
- Bad, because all users logged out

### Invalidate compromised refresh token
- Good, because malicious actor denied access
- Good, because users remain logged in

### Invalidate no tokens
- Bad, because malicious actor retains access
