from unittest.mock import Mock, patch

from auth.infrastructure.sendgrid_client import SendgridClient


@patch("auth.infrastructure.sendgrid_client.SendGridAPIClient")
@patch("auth.infrastructure.sendgrid_client.Mail")
def test_send_template_message_build_mail_instance(mail_mock, _):
    to = "to@email.com"
    subject = "A subject"
    template_id = "mock_template_id"
    template_data = dict(name="Foo")

    SendgridClient().send_template_message(
        to=to, subject=subject, template_id=template_id, template_data=template_data
    )

    mail_mock.assert_called_once_with(
        from_email="no-reply@em7936.nicolaszein.dev", to_emails=to
    )
    assert mail_mock().template_id == template_id
    assert mail_mock().dynamic_template_data == {
        **template_data,
        **{"subject": subject},
    }


@patch("auth.infrastructure.sendgrid_client.Mail")
@patch("auth.infrastructure.sendgrid_client.SendGridAPIClient")
def test_send_template_message_call_client(client_api_mock, mail_mock):
    to = "to@email.com"
    subject = "A subject"
    template_id = "mock_template_id"
    template_data = dict(name="Foo")
    mail_instance = Mock()
    mail_mock.return_value = mail_instance

    SendgridClient().send_template_message(
        to=to, subject=subject, template_id=template_id, template_data=template_data
    )

    client_api_mock().send.assert_called_once_with(mail_instance)
