import uuid

from jose import jwt

from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.session import Session
from auth.infrastructure.entity.user import User
from auth.infrastructure.password import Password
from auth.infrastructure.repository.session import SessionRepository
from auth.infrastructure.repository.user import UserRepository
from auth.infrastructure.token import Token
from auth.view.function.sign_out import handle


def test_sign_out_ok(database):
    password = 'a-secret'
    hashed_password = Password.hash_password(password)
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password=hashed_password,
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    refresh_token = Token().generate_refresh_token(user_id=str(user.id))
    session = Session(user_id=user.id, refresh_token=refresh_token)
    SessionRepository().create(session)
    access_token = Token().generate_token(user_id=str(user.id), session_id=str(session.id))
    event = {
        'headers': {
            'Authorization': f'Bearer {access_token}'
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 204
    assert not SessionRepository().fetch_by_id(session.id)


def test_sign_out_with_invalid_token(database):
    access_token = jwt.encode(
        dict(user_id=str(uuid.uuid4())),
        'wrong_jwt_secret_token',
        algorithm='HS256'
    )
    event = {
        'headers': {
            'Authorization': f'Bearer {access_token}'
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 401


def test_sign_out_with_no_authorization_header(database):
    event = {
        "headers": {}
    }

    result = handle(event, None)

    assert result['statusCode'] == 401


def test_sign_out_with_empty_authorization_header(database):
    event = {
        'headers': {
            'Authorization': ''
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 401


def test_sign_out_without_token_type(database):
    event = {
        'headers': {
            'Authorization': 'token'
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 401


def test_sign_out_with_invalid_jwt_token(database):
    event = {
        'headers': {
            'Authorization': 'Bearer invalid-token'
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 401
