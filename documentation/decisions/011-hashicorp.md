[arad](../../../../) / [documentation](../README.md) / [decisions](./README.md)

# Hashicorp Tools for Deployment and Infrastructure Configuration

**Date**: 2022-08-07

**Decider(s)**: [@jasoncolburne](https://github.com/jasoncolburne)

**Status**: decided

We require deployment and configuration tooling. It should be easy to use.

## Considered Options
- No Tools
- Kubernetes
- Hashicorp (Nomad/Consul/Vault)


## Decision Outcome

**Chosen Option**: Hashicorp, for ease of configuration and use, and because manual deployment isn't fun.

[Reference](https://cloud.netapp.com/blog/cvo-blg-kubernetes-vs-nomad-understanding-the-tradeoffs)
