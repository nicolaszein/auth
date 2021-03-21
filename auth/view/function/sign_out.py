from jwt import DecodeError, InvalidSignatureError

from auth.application.user_service import UserService
from auth.view.helper import build_error_response, build_success_response


def handle(event, context):
    header_authorization = event.get('headers', {}).get('Authorization')
    invalid_credentials_response = build_error_response(
        status_code=401,
        code='INVALID_CREDENTIALS',
        message='Invalid credentials.',
    )

    if not header_authorization:
        return invalid_credentials_response

    try:
        _, access_token = header_authorization.split('Bearer ')
    except ValueError:
        return invalid_credentials_response

    try:
        UserService().sign_out(access_token=access_token)
    except (InvalidSignatureError, DecodeError):
        return invalid_credentials_response

    return build_success_response(status_code=204)
