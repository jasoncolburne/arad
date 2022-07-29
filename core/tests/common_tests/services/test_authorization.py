import datetime
import unittest.mock
import uuid

import jose
import pytest

import common.datatypes.domain
import common.datatypes.exception
import common.services.authorization


def test_verify_and_parse_token__calls_jose() -> None:
    user_id = uuid.uuid4()
    token = "access_token"
    payload = {
        "sub": str(user_id),
        "exp": int(
            (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).timestamp()
        ),
        "scope": common.datatypes.domain.Role.READER.value,
    }
    authorization_service = common.services.authorization.AuthorizationService()

    with unittest.mock.patch("common.services.authorization.jwt.decode") as jwt_decode:
        jwt_decode.return_value = payload
        result = authorization_service.verify_and_parse_token(token=token)
        jwt_decode.assert_called_once_with(
            token, unittest.mock.ANY, algorithms=["ES256"]
        )

    assert result == common.datatypes.domain.Token(**payload)


def test_verify_and_parse_token__raises_for_jose() -> None:
    token = "access_token"
    authorization_service = common.services.authorization.AuthorizationService()

    with pytest.raises(common.datatypes.exception.UnauthorizedException):
        with unittest.mock.patch(
            "common.services.authorization.jwt.decode"
        ) as jwt_decode:
            jwt_decode.side_effect = jose.JWTError()
            authorization_service.verify_and_parse_token(token=token)
            jwt_decode.assert_called_once_with(
                token, unittest.mock.ANY, algorithms=["ES256"]
            )


def test_verify_and_parse_token__raises_if_expired() -> None:
    user_id = uuid.uuid4()
    token = "access_token"
    payload = {
        "sub": str(user_id),
        "exp": int(
            (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).timestamp()
        ),
        "scope": common.datatypes.domain.Role.READER.value,
    }
    authorization_service = common.services.authorization.AuthorizationService()

    with pytest.raises(common.datatypes.exception.UnauthorizedException):
        with unittest.mock.patch(
            "common.services.authorization.jwt.decode"
        ) as jwt_decode:
            jwt_decode.return_value = payload
            authorization_service.verify_and_parse_token(token=token)


def test_verify_and_parse_token__raises_if_expiration_missing() -> None:
    user_id = uuid.uuid4()
    token = "access_token"
    payload = {"sub": str(user_id), "scope": common.datatypes.domain.Role.READER.value}
    authorization_service = common.services.authorization.AuthorizationService()

    with pytest.raises(common.datatypes.exception.UnauthorizedException):
        with unittest.mock.patch(
            "common.services.authorization.jwt.decode"
        ) as jwt_decode:
            jwt_decode.return_value = payload
            authorization_service.verify_and_parse_token(token=token)
