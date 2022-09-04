import uuid
import typing

import sqlalchemy
import sqlalchemy.dialects.postgresql.base
import sqlalchemy.sql.sqltypes
import sqlalchemy.sql.type_api


# Use the following as the value of server_default for primary keys of type GUID
GUID_SERVER_DEFAULT_POSTGRESQL = sqlalchemy.DefaultClause(
    sqlalchemy.text("gen_random_uuid()")
)

UUIDTypeDecorator = sqlalchemy.sql.type_api.TypeDecorator[uuid.UUID]


class GUID(UUIDTypeDecorator):  # pylint: disable=abstract-method
    impl = sqlalchemy.sql.sqltypes.CHAR
    cache_ok = True

    @typing.no_type_check
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @typing.no_type_check
    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(sqlalchemy.dialects.postgresql.base.UUID())

    @typing.no_type_check
    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        return str(value)

    @typing.no_type_check
    def process_result_value(self, value, dialect):
        if value is None:
            return value

        if not isinstance(value, uuid.UUID):  # pragma: no branch
            value = uuid.UUID(value)

        return value
