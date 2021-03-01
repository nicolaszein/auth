import json

from auth.domain.user import User
from auth.infrastructure.entity.user import User as UserEntity
from auth.infrastructure.repository.user import UserRepository
from auth.view.function.create_reset_password_token import handle


def test_create_reset_password_token_ok(database):
    user = User(full_name='Foo Bar', email='foo.bar@email.com', password='a-secret')
    entity = UserEntity.from_domain(user)
    UserRepository().create(entity)
    request_body = {
        'email': user.email,
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 204
    assert entity.reset_password_token
    assert entity.reset_password_token_created_at


def test_create_reset_password_token_with_not_found_user(database):
    request_body = {
        'email': 'not_found@email.com',
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 204


def test_create_reset_password_token_with_null_email(database):
    request_body = {
        'email': None,
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'email' in result['body']


def test_create_reset_password_token_with_invalid_email(database):
    request_body = {
        'email': 'invalid-email',
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'email' in result['body']
