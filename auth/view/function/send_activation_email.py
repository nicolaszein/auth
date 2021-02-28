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
        if not event_name == 'activation_created':
            return None

        user_id = body['payload']['user_id']
        code = body['payload']['code']
        UserService().send_activation_email(user_id=user_id, activation_code=code)
