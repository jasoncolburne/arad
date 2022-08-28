# pylint: disable=unused-import,wrong-import-position
import sys

sys.path.append("/app/")

import sqlalchemy.ext.asyncio
import sqlalchemy.orm

import database
import identity.orchestrations


async_engine = database.global_database_manager.get_engine()
print("db = await async_engine.connect()  # don't forget to close")
