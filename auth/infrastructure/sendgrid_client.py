from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from auth.settings import SENDGRID_API_KEY

FROM_EMAIL = 'no-reply@nicolaszein.dev'


class SendgridClient:

    def __init__(self):
        self.__client = SendGridAPIClient(SENDGRID_API_KEY)

    def send_template_message(self, to, subject, template_id, template_data, from_email=FROM_EMAIL):
        template_data = template_data.copy()
        message = Mail(
            from_email=from_email,
            to_emails=to,
        )
        template_data['subject'] = subject
        message.dynamic_template_data = template_data
        message.template_id = template_id

        response = self.__client.send(message)
        return response
