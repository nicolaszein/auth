import json

from auth.view.function.sign_up import handle


def test_sign_up_ok(database):
    request_body = {
        'full_name': 'Foo Bar',
        'email': 'foo.bar@email.com',
        'password': 'a-secret'
    }
    event = {
        "body": json.dumps(request_body),
    }
    result = handle(event, None)

    assert result['statusCode'] == 204


def test_sign_up_with_invalid_json(database):
    event = {
        "body": '{invalid}',
    }
    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'BAD_REQUEST' in result['body']


def test_sign_up_with_invalid_input(database):
    event = {
        "body": None,
    }
    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'INPUT_VALIDATION_ERROR' in result['body']


def test_sign_up_with_no_full_name(database):
    request_body = {
        'full_name': None,
        'email': 'foo.bar@email.com',
        'password': 'a-secret'
    }
    event = {
        "body": json.dumps(request_body),
    }
    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'full_name' in result['body']


def test_sign_up_with_short_full_name(database):
    request_body = {
        'full_name': 'fo',
        'email': 'foo.bar@email.com',
        'password': 'a-secret'
    }
    event = {
        "body": json.dumps(request_body),
    }
    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'full_name' in result['body']


def test_sign_up_with_no_email(database):
    request_body = {
        'full_name': 'fo',
        'email': None,
        'password': 'a-secret'
    }
    event = {
        "body": json.dumps(request_body),
    }
    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'email' in result['body']


def test_sign_up_with_invalid_email(database):
    request_body = {
        'full_name': 'fo',
        'email': 'invalid-email',
        'password': 'a-secret'
    }
    event = {
        "body": json.dumps(request_body),
    }
    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'email' in result['body']


def test_sign_up_with_no_password(database):
    request_body = {
        'full_name': 'fo',
        'email': 'foo.bar@email.com',
        'password': None
    }
    event = {
        "body": json.dumps(request_body),
    }
    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'password' in result['body']


def test_sign_up_with_short_password(database):
    request_body = {
        'full_name': 'fo',
        'email': 'foo.bar@email.com',
        'password': 'ab'
    }
    event = {
        "body": json.dumps(request_body),
    }
    result = handle(event, None)

    assert result['statusCode'] == 400
    assert 'password' in result['body']
