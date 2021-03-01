import json

from auth.application.user_service import UserService


def handle(event, context):
    records = event['Records']

    for record in records:
        try:
            body = json.loads(record.get("body") or "{}")
        except ValueError:
            continue

        event_name = body.get('name', '')
        if not event_name == 'reset_password_token_created':
            return None

        user_id = body['payload']['user_id']
        token = body['payload']['token']
        UserService().send_reset_password_email(user_id=user_id, reset_password_token=token)
