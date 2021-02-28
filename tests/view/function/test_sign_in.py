import json

from auth.domain.user_status import UserStatus
from auth.infrastructure.entity.user import User
from auth.infrastructure.password import Password
from auth.infrastructure.repository.user import UserRepository
from auth.settings import TOKEN_EXPIRATION_TIME
from auth.view.function.sign_in import handle


def test_sign_in_ok(database):
    password = 'a-secret'
    hashed_password = Password.hash_password(password)
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password=hashed_password,
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    request_body = {
        'email': 'foo.bar@email.com',
        'password': password
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    response_body = json.loads(result['body'])
    assert result['statusCode'] == 200
    assert response_body['access_token']
    assert response_body['refresh_token']
    assert response_body['expires_in'] == TOKEN_EXPIRATION_TIME
    assert response_body['token_type'] == 'bearer'


def test_sign_in_with_inactive_user(database):
    password = 'a-secret'
    hashed_password = Password.hash_password(password)
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password=hashed_password,
        status=UserStatus.INACTIVE.value
    )
    UserRepository().create(user)
    request_body = {
        'email': 'foo.bar@email.com',
        'password': password
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 401
    assert 'User is not activated' in result['body']


def test_sign_in_with_wrong_password(database):
    password = 'a-secret'
    hashed_password = Password.hash_password(password)
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password=hashed_password,
        status=UserStatus.ACTIVE.value
    )
    UserRepository().create(user)
    request_body = {
        'email': 'foo.bar@email.com',
        'password': 'wrong-password'
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 401
    assert 'Invalid credentials' in result['body']


def test_sign_in_with_user_not_found(database):
    password = 'a-secret'
    request_body = {
        'email': 'foo.bar@email.com',
        'password': password
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 401
    assert 'Invalid credentials' in result['body']


def test_sign_in_with_no_email(database):
    request_body = {
        'email': None,
        'password': 'a-secret'
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'email' in result['body']


def test_sign_in_with_invalid_email(database):
    request_body = {
        'email': 'invalid-email',
        'password': 'a-secret'
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'email' in result['body']


def test_sign_in_with_no_password(database):
    request_body = {
        'email': 'foo.bar@email.com',
        'password': None
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'password' in result['body']
