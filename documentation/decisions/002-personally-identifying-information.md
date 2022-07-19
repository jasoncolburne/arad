# Forbid Collection of Personally Identifying Information

**Date**: 2022-07-19

**Deciders**: [@jasoncolburne](https://github.com/jasoncolburne), [@Stampnerd](https://github.com/Stampnerd)

**Status**: decided

We would like to minimie our impact in case of a breach.

It is proposed that by not collecting personally identifying information (PII), we protect our users and minimize our
risk.


## Considered Options
- Forbid collecting PII
- Allow collecting PII


## Decision Outcome

**Chosen Option**: Forbid collecting PII, for reasons below.

**Positive Consequences**:
- Reduces risk to users in case of breach

**Potential Negative Consequences**:
- Cannot access richer user analytics in the future


## Pros and Cons of the Options

### Forbid collecting PII
- Good, because our users' risk is minimized
- Bad, because we will not be able to derive useful user analytics in the future

### Allow collecting PII
- Good, because we will be able to derive user analytics in the future (but we question their use)
- Bad, because users' personal information will be at greater risk of exposure
