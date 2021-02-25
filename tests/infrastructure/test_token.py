import datetime
from unittest.mock import patch

import jwt
import pytest
from freezegun import freeze_time

from auth.infrastructure.token import Token
from auth.settings import JWT_SECRET_TOKEN, TOKEN_EXPIRATION_TIME


@freeze_time('2019-01-01 00:00:00')
@patch('auth.infrastructure.token.jwt')
def test_generate_token(jwt_mock):
    exp = datetime.datetime.now() + datetime.timedelta(seconds=TOKEN_EXPIRATION_TIME)
    iat = datetime.datetime.now()
    iss = 'auth_svc'
    jwt_mock.encode.return_value = 'token'
    expected_payload = {
        'exp': datetime.datetime.timestamp(exp),
        'iat': datetime.datetime.timestamp(iat),
        'iss': iss,
        'session_id': 'session-id',
        'user_id': 'user-id'
    }

    token = Token().generate_token(user_id='user-id', session_id='session-id')

    jwt_mock.encode.assert_called_once_with(
        expected_payload,
        JWT_SECRET_TOKEN,
        algorithm='HS256'
    )
    assert token == 'token'


@freeze_time('2019-01-01 00:00:00')
@patch('auth.infrastructure.token.jwt')
def test_generate_token_without_expire_in(jwt_mock):
    iat = datetime.datetime.now()
    iss = 'auth_svc'
    jwt_mock.encode.return_value = 'token'
    expected_payload = {
        'iat': datetime.datetime.timestamp(iat),
        'iss': iss,
        'session_id': 'session-id',
        'user_id': 'user-id'
    }

    token = Token().generate_token(user_id='user-id', session_id='session-id', expire_in=None)

    jwt_mock.encode.assert_called_once_with(
        expected_payload,
        JWT_SECRET_TOKEN,
        algorithm='HS256'
    )
    assert token == 'token'


@freeze_time('2019-01-01 00:00:00')
@patch('auth.infrastructure.token.jwt')
def test_generate_refresh_token(jwt_mock):
    iat = datetime.datetime.now()
    iss = 'auth_svc'
    jwt_mock.encode.return_value = 'refresh-token'
    expected_payload = {
        'iat': datetime.datetime.timestamp(iat),
        'iss': iss,
        'user_id': 'user-id'
    }

    refresh_token = Token().generate_refresh_token(user_id='user-id')

    jwt_mock.encode.assert_called_once_with(
        expected_payload,
        JWT_SECRET_TOKEN,
        algorithm='HS256'
    )
    assert refresh_token == 'refresh-token'


@patch('auth.infrastructure.token.jwt')
def test_validate_token(jwt_mock):
    token = Token().generate_token(user_id='user-id', session_id='session-id')

    Token().validate_token(token)

    jwt_mock.decode.assert_called_once_with(
        token,
        JWT_SECRET_TOKEN,
        algorithms=['HS256']
    )


def test_validate_expired_token():
    with freeze_time('2019-01-01 00:00:00'):
        token = Token().generate_token(user_id='user-id', session_id='session-id')

    with pytest.raises(jwt.ExpiredSignatureError):
        Token().validate_token(token)


def test_validate_token_with_invalid_signature():
    token = jwt.encode(
        dict(invalid='signature'),
        'invalid_signature',
        algorithm='HS256'
    )

    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        Token().validate_token(token)
