[arad](../../../../) / [documentation](../) / [design](./)

# Endpoint Design

Endpoints are easy to write in FastAPI. Here is an example:

```python
@app.put("/role", response_model=RoleResponse)
@require_authorization(Role.ADMINISTRATOR)
async def assign_role(
    request: RoleRequest,
    token: str = Depends(oauth2_scheme),
    database: Session = Depends(get_session),
):
    role_service = RoleService(database=database)
    user_service = UserService(database=database)

    user = await user_service.get(user_id=request.user_id)

    # this admin function isn't critical and the ui should protect us from most edge cases so we'll just let these
    # calls explode if for instance the role has already been assigned to the user (possible with two tabs open)
    if request.action == RoleAction.ASSIGN:
        role = await role_service.assign_for_user(user=user, role=request.role)
    elif request.action == RoleAction.REVOKE:
        role = await role_service.revoke_for_user(user=user, role=request.role)
    else:
        # this code should be unreachable
        raise Exception()

    # TODO: log user out by removing refresh tokens

    return {"role": role}
```

This code is saying:

- `@app.put()`: create a route at /role for PUT requests and listen for requests to respond with a RoleResponse message
- `@require_authorization()`: force the end user to use a scoped access token for authorizing access to this resource

The rest of the code simply composes service code to accomplish the task at hand. Note that all endpoints are
asynchronous and service calls typically require an `await` if they end up poking any actual resources.

## OpenAPI Spec

An OpenAPI Spec is generated as part of FastAPI (disabled outside development). To find it, simply make a GET request to
http://localhost:800x/openapi.json, where the port is defined in `docker-compose.yml`.

## Live Documentation

Live documentation is available at http://localhost:800x/docs/, where the port is defined in `docker-compose.yml`.
