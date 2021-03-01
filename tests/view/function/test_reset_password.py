import datetime
import json

from auth.domain.user import User
from auth.infrastructure.entity.user import User as UserEntity
from auth.infrastructure.repository.user import UserRepository
from auth.view.function.reset_password import handle


def test_reset_password_ok(database):
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret'
    ).create_reset_password_token()
    entity = UserEntity.from_domain(user)
    UserRepository().create(entity)
    request_body = {
        'new_password': 'new-password',
    }
    event = {
        'body': json.dumps(request_body),
        'pathParameters': {
            'reset_password_token': user.reset_password_token
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 204


def test_reset_password_with_expired_token(database):
    expires_in = datetime.datetime(2020, 1, 1)
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='a-secret',
        reset_password_token='token',
        reset_password_token_created_at=expires_in
    )
    entity = UserEntity.from_domain(user)
    UserRepository().create(entity)
    request_body = {
        'new_password': 'new-password',
    }
    event = {
        'body': json.dumps(request_body),
        'pathParameters': {
            'reset_password_token': 'token'
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'Reset password token expired' in result['body']


def test_reset_password_with_not_found_token(database):
    request_body = {
        'new_password': 'new-password',
    }
    event = {
        'body': json.dumps(request_body),
        'pathParameters': {
            'reset_password_token': 'not-found-token'
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 404
    assert 'Reset password token not found' in result['body']


def test_reset_password_with_empty_new_password(database):
    request_body = {
        'new_password': '',
    }
    event = {
        'body': json.dumps(request_body),
        'pathParameters': {
            'reset_password_token': 'token'
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'new_password' in result['body']


def test_reset_password_with_null_new_password(database):
    request_body = {
        'new_password': None,
    }
    event = {
        'body': json.dumps(request_body),
        'pathParameters': {
            'reset_password_token': 'token'
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'new_password' in result['body']


def test_reset_password_with_new_password_shorten_than_4(database):
    request_body = {
        'new_password': '123',
    }
    event = {
        'body': json.dumps(request_body),
        'pathParameters': {
            'reset_password_token': 'token'
        }
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'new_password' in result['body']
