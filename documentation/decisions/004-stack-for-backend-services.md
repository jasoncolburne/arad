# fastapi/sqlmodel/asyncpg/aioredis for Back-end Stack

**Date**: 2022-07-19

**Decider**: [@jasoncolburne](https://github.com/jasoncolburne)

**Status**: decided

We need to choose a back-end stack. Factors to consider are complexity, performance and scalability.


## Considered Options
- fastapi/sqlmodel/asyncpg/aioredis
- rails/activerecord on postgres/redis
- flask/sqlalchemy/psycopg2/redis

## Decision Outcome

**Chosen Option**: fastapi

## Pros and Cons of the Options

### fastapi
- Good, because asynchronous so performant and efficient (should scale well)
- Good, because the fastapi framework is very lightweight (not complex)
- Good, because there is a significant amount of work already done using this stack
- Bad, because async is a bit trickier

### rails
- Good, because ruby is guessable and generally a productive language
- Good, because rails has a proven track record
- Bad, because rails is not as performant as most other solutions
- Bad, because rails is more difficult to scale

### flask
- Good, because the framework is very lightweight (not complex)