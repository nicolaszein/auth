from auth.application.user_service import UserService
from auth.infrastructure.exception import SessionNotFound
from auth.view.decorator import validate_request_body
from auth.view.helper import build_error_response, build_success_response
from auth.view.resource.refresh_session_request import RefreshSessionRequest
from auth.view.resource.session_response import SessionResponse


@validate_request_body(RefreshSessionRequest)
def handle(request, event, context):
    try:
        session = UserService().refresh_session(refresh_token=request.refresh_token)
    except SessionNotFound:
        return build_error_response(
            status_code=401,
            code='INVALID_CREDENTIALS',
            message='Invalid credentials.',
        )

    response = build_success_response(
        status_code=200,
        body=SessionResponse.from_domain(session).json()
    )

    return response
