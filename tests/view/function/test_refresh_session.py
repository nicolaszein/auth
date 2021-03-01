import json
import uuid

from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.session import Session
from auth.infrastructure.entity.user import User
from auth.infrastructure.repository.session import SessionRepository
from auth.infrastructure.repository.user import UserRepository
from auth.settings import TOKEN_EXPIRATION_TIME
from auth.view.function.refresh_session import handle


def test_refresh_session_ok(database):
    refresh_token = str(uuid.uuid4())
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    session = Session(user_id=user.id, refresh_token=refresh_token)
    SessionRepository().create(session)
    request_body = {
        'refresh_token': session.refresh_token,
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    response_body = json.loads(result['body'])
    assert result['statusCode'] == 200
    assert response_body['access_token']
    assert response_body['refresh_token'] == refresh_token
    assert response_body['expires_in'] == TOKEN_EXPIRATION_TIME
    assert response_body['token_type'] == 'bearer'


def test_refresh_session_with_not_found_refresh_token(database):
    request_body = {
        'refresh_token': 'not_found_refresh_token',
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 401
    assert 'Invalid credentials' in result['body']


def test_refresh_session_with_empty_refresh_token(database):
    request_body = {
        'refresh_token': '',
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'refresh_token' in result['body']


def test_refresh_session_with_null_refresh_token(database):
    request_body = {
        'refresh_token': None,
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'refresh_token' in result['body']
