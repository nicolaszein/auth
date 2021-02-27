import json
from datetime import datetime

from auth.domain.activation import Activation
from auth.domain.user import User
from auth.infrastructure.entity.user import User as UserEntity
from auth.infrastructure.repository.user import UserRepository
from auth.view.function.activate import handle


def test_activate_ok(database):
    user = User(full_name='Foo Bar', email='foo.bar@email.com', password='a-secret')
    user.create_activation()
    code = user.activations[0].code
    entity = UserEntity.from_domain(user)
    UserRepository().create(entity)
    request_body = {
        'code': code,
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 204


def test_activate_with_expired_code(database):
    created_at = datetime(2020, 1, 1)
    user = User(full_name='Foo Bar', email='foo.bar@email.com', password='a-secret')
    activation = Activation(user=user, created_at=created_at)
    user.activations.append(activation)
    code = user.activations[0].code
    entity = UserEntity.from_domain(user)
    UserRepository().create(entity)
    request_body = {
        'code': code,
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'Activation Code expired' in result['body']


def test_activate_with_not_found_code(database):
    request_body = {
        'code': 'not_found_code',
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 404
    assert 'Activation Code not found' in result['body']


def test_activate_with_empty_code(database):
    request_body = {
        'code': '',
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'code' in result['body']


def test_activate_with_null_code(database):
    request_body = {
        'code': None,
    }
    event = {
        "body": json.dumps(request_body),
    }

    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'code' in result['body']
