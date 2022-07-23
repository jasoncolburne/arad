# [short title of solved problem and solution]

**Date**: 2022-07-23

**Decider(s)**: [@jasoncolburne](https://github.com/jasoncolburne), [@dalejh](https://github.com/dalejh) 

**Status**: decided

We have the option of tacking comments onto reviews because there is a one to one mapping. We want to know if this is
actually the best architectural decision for this project.

## Considered Options
- Use a Comments table
- Embed Comments in Reviews

## Decision Outcome

**Chosen Option**: Use a Comments Table

**Positive Consequences**:
- Allows us to more cleanly track impressions and sentiment about individual comments

**Negative Consequences**:
- More complex in general
