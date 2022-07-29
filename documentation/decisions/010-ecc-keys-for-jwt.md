[arad](../../../../) / [documentation](../README.md) / [decisions](./README.md)

# Asymmetric EC Signing Algorithm for JWTs

**Date**: 2022-07-29

**Decider(s)**: [@jasoncolburne](https://github.com/jasoncolburne)

**Status**: decided

We have three classes of solutions when considering the signing algorithm for JSON Web Tokens.


## Considered Options
- Symmetric Key (HMAC?)
- RSA
- ECC


## Decision Outcome

**Chosen Option**: ECC

**Positive Consequences**:
- Quantum Resistant
- Authorization Uses Public Key


## Pros and Cons of the Options

### Symmetric Key
- Good, because examples are readily available
- Bad, because the signing key must be shared

### RSA
- Good, because the signing key need not be shared
- Bad, because the algorithm is not quantum resistant

### ECC
- Good, because the algorithm is quantum resistant
- Good, because the signing key need not be shared

