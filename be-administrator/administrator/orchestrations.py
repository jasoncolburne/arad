import typing

import sqlmodel

import administrator.services.user


async def arad_users(
    email_filter: str,
    page: int | None,
    database: sqlmodel.Session | None,
    user_service: administrator.services.user.UserService | None,
) -> dict[str, typing.Any]:
    if user_service is None and database is None:
        raise Exception()

    if user_service is None:
        user_service = administrator.services.user.UserService(database=database)

    user_page = await user_service.page(email_filter=email_filter, number=page)

    return user_page.dict()
