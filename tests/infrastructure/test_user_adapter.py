import uuid
from dataclasses import replace
from unittest.mock import MagicMock, Mock, patch

import pytest

from auth.domain.user import User
from auth.infrastructure.entity.session import Session
from auth.infrastructure.exception import SessionNotFound, UserNotFound
from auth.infrastructure.user_adapter import UserAdapter
from auth.settings import ACTIVATION_EMAIL_TEMPLATE_ID, RESET_PASSWORD_EMAIL_TEMPLATE_ID


@patch('auth.infrastructure.user_adapter.User')
@patch('auth.infrastructure.user_adapter.UserRepository')
def test_create(user_repository_mock, user_entity_mock):
    user = User(
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    persisted_user = replace(user, id=uuid.uuid4())
    user_entity = MagicMock()
    user_repository_mock().create.return_value = user_entity
    user_entity.to_domain.return_value = persisted_user

    result = UserAdapter().create(user)

    assert result == persisted_user
    user_entity_mock.from_domain.assert_called_once_with(user)


@patch('auth.infrastructure.user_adapter.User')
@patch('auth.infrastructure.user_adapter.UserRepository')
def test_update(user_repository_mock, user_entity_mock):
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    user_entity = MagicMock()
    user_repository_mock().update.return_value = user_entity
    user_entity.to_domain.return_value = user

    result = UserAdapter().update(user=user)

    assert result == user
    user_entity_mock.from_domain.assert_called_once_with(user)


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_id(user_repository_mock):
    id = uuid.uuid4()
    user = User(
        id=id,
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    user_entity = MagicMock()
    user_repository_mock().fetch_by_id.return_value = user_entity
    user_entity.to_domain.return_value = user

    result = UserAdapter().fetch_by_id(id=id)

    assert result == user


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_id_with_user_not_found(user_repository_mock):
    user_repository_mock().fetch_by_id.return_value = None

    with pytest.raises(UserNotFound):
        UserAdapter().fetch_by_id(id=uuid.uuid4())


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_email(user_repository_mock):
    id = uuid.uuid4()
    email = 'foo.bar@email.com'
    user = User(
        id=id,
        full_name='Foo Bar',
        email=email,
        password='hashed_password'
    )
    user_entity = MagicMock()
    user_repository_mock().fetch_by_email.return_value = user_entity
    user_entity.to_domain.return_value = user

    result = UserAdapter().fetch_by_email(email=email)

    assert result == user


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_email_with_user_not_found(user_repository_mock):
    user_repository_mock().fetch_by_email.return_value = None

    with pytest.raises(UserNotFound):
        UserAdapter().fetch_by_email(email='foo.bar@email.com')


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_activation_code(user_repository_mock):
    user = User(
        id=uuid.uuid4(),
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    user_entity = MagicMock()
    user_repository_mock().fetch_by_activation_code.return_value = user_entity
    user_entity.to_domain.return_value = user
    code = '123'

    result = UserAdapter().fetch_by_activation_code(code=code)

    assert result == user


@patch('auth.infrastructure.user_adapter.UserRepository')
def test_fetch_by_activation_code_with_user_not_found(user_repository_mock):
    code = '123'
    user_repository_mock().fetch_by_activation_code.return_value = None

    with pytest.raises(UserNotFound):
        UserAdapter().fetch_by_activation_code(code=code)


@patch('auth.infrastructure.user_adapter.Token')
@patch('auth.infrastructure.user_adapter.SessionRepository')
def test_create_session(session_repository_mock, token_mock):
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    session = Session(id=uuid.uuid4(), user_id=user_id, refresh_token='refresh_token')
    session_repository_mock().create.return_value = session
    token_mock().generate_token.return_value = 'access_token'
    token_mock().generate_refresh_token.return_value = 'refresh_token'

    result = UserAdapter().create_session(user)

    assert result.user == user
    assert result.access_token == 'access_token'
    assert result.refresh_token == 'refresh_token'
    token_mock().generate_refresh_token.assert_called_once_with(user_id=str(user_id))
    token_mock().generate_token.assert_called_once_with(
        user_id=str(user_id),
        session_id=str(session.id)
    )


@patch('auth.infrastructure.user_adapter.Token')
@patch('auth.infrastructure.user_adapter.SessionRepository')
def test_refresh_session(session_repository_mock, token_mock):
    user_id = uuid.uuid4()
    refresh_token = 'refresh_token'
    user = User(
        id=user_id,
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )
    session = Session(id=uuid.uuid4(), user_id=user_id, refresh_token=refresh_token)
    session.user = user
    session_repository_mock().fetch_by_refresh_token.return_value = session
    token_mock().generate_token.return_value = 'refreshed_access_token'

    result = UserAdapter().refresh_session(refresh_token)

    assert result.user == user
    assert result.access_token == 'refreshed_access_token'
    assert result.refresh_token == refresh_token
    token_mock().generate_token.assert_called_once_with(
        user_id=str(user_id),
        session_id=str(session.id)
    )


@patch('auth.infrastructure.user_adapter.SessionRepository')
def test_refresh_session_with_session_not_found(session_repository_mock):
    refresh_token = 'refresh_token'
    session_repository_mock().fetch_by_refresh_token.return_value = None

    with pytest.raises(SessionNotFound):
        UserAdapter().refresh_session(refresh_token)


@patch('auth.infrastructure.user_adapter.SessionRepository')
def test_delete_session(session_repository_mock):
    session_id = uuid.uuid4()
    session = Mock()
    session_repository_mock().fetch_by_id.return_value = session

    UserAdapter().delete_session(session_id=session_id)

    session_repository_mock().fetch_by_id.assert_called_once_with(id=session_id)
    session_repository_mock().delete.assert_called_once_with(session=session)


@patch('auth.infrastructure.user_adapter.SendgridClient')
def test_send_activation_email(sendgrid_client_mock):
    code = uuid.uuid4()
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )

    UserAdapter().send_activation_email(user=user, activation_code=code)

    sendgrid_client_mock().send_template_message.assert_called_once_with(
        to=user.email,
        subject='Por favor, confirme seu endereço de email',
        template_id=ACTIVATION_EMAIL_TEMPLATE_ID,
        template_data=dict(first_name=user.first_name, code=code)
    )


@patch('auth.infrastructure.user_adapter.SendgridClient')
def test_send_reset_password_email(sendgrid_client_mock):
    token = str(uuid.uuid4())
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        full_name='Foo Bar',
        email='foo.bar@email.com',
        password='hashed_password'
    )

    UserAdapter().send_reset_password_email(user=user, reset_password_token=token)

    sendgrid_client_mock().send_template_message.assert_called_once_with(
        to=user.email,
        subject='Redefinir Senha',
        template_id=RESET_PASSWORD_EMAIL_TEMPLATE_ID,
        template_data=dict(first_name=user.first_name, token=token)
    )
