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
        if not event_name == 'user_created':
            return None

        user_id = body['payload']['user_id']
        UserService().create_activation(user_id=user_id)
