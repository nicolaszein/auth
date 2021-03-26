from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError

from auth.application.user_service import UserService
from auth.infrastructure.token import Token
from auth.view.helper import build_error_response, build_success_response
from auth.view.resource.user_response import UserResponse


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
        decoded_token = Token().validate_token(access_token)
    except (InvalidSignatureError, DecodeError, ExpiredSignatureError):
        return invalid_credentials_response

    user = UserService().fetch_by_id(decoded_token['user_id'])

    return build_success_response(status_code=200, body=UserResponse.from_domain(user).json())
