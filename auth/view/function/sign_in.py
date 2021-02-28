from auth.application.exception import InvalidCredentials, UserNotActivated
from auth.application.user_service import UserService
from auth.infrastructure.exception import UserNotFound
from auth.view.decorator import validate_request_body
from auth.view.helper import build_error_response
from auth.view.resource.session_response import SessionResponse
from auth.view.resource.sign_in_request import SignInRequest


@validate_request_body(SignInRequest)
def handle(request, event, context):
    try:
        session = UserService().sign_in(
            email=request.email,
            password=request.password
        )
    except UserNotActivated:
        return build_error_response(
            status_code=401,
            code='USER_NOT_ACTIVATED',
            message='User is not activated. Please confirm your e-mail.',
        )
    except (InvalidCredentials, UserNotFound):
        return build_error_response(
            status_code=401,
            code='INVALID_CREDENTIALS',
            message='Invalid credentials.',
        )

    response = {
        'statusCode': 200,
        'body': SessionResponse.from_domain(session).json()
    }

    return response
