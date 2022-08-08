[arad](../../../../) / [documentation](../README.md)

# Decisions

See [this Wikipedia page](https://en.wikipedia.org/wiki/Architectural_decision)
and [this SpeakerDeck page](https://speakerdeck.com/vanto/a-brief-introduction-to-architectural-decision-records)
for motivation behind this directory.

Many of these were recorded days or weeks after they were decided, and the dates do not reflect that. The content
itself is more important so I don't intend to do archaeology to figure out the correct dates.

- [001: 120 Character Maximum Line Length for Source Files](./001-line-length.md)
- [002: Forbid Collection of Personally Identifying Information](./002-personally-identifying-information.md)
- [003: Provide Mechanism to Invalidate Refresh Token](./003-invalidate-refresh-token.md)
- [004: fastapi/sqlmodel/asyncpg/aioredis for Back-end Stack](./004-stack-for-backend-services.md)
- [005: Comment Table to Establish Sentiment Metric](./005-use-comment-table.md)
- [006: Isolate User Data in Identity](./006-isolate-user-data-in-identity.md)
- [007: Employ End-to-End Testing](./007-employ-end-to-end-testing.md)
- [008: Read-Only Access for Reader Service](./008-read-only-access-for-reader.md)
- [009: Default Docker Compose for Local Development](./009-default-docker-compose-for-local.md)
- [010: ECC Keys for JWT Signatures](./010-ecc-keys-for-jwt.md)
- [011: Hashicorp Tooling for Deployment and Configuration](./011-hashicorp.md)
