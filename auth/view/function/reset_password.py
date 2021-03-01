from auth.application.user_service import UserService
from auth.domain.exception import ResetPasswordTokenExpired
from auth.infrastructure.exception import UserNotFound
from auth.view.decorator import validate_request_body
from auth.view.helper import build_error_response
from auth.view.resource.reset_password_request import ResetPasswordRequest


@validate_request_body(ResetPasswordRequest)
def handle(request, event, context):
    reset_password_token = event.get('pathParameters', {}).get('reset_password_token')

    try:
        UserService().reset_password(
            new_password=request.new_password,
            reset_password_token=reset_password_token
        )
    except UserNotFound:
        return build_error_response(
            status_code=404,
            code='RESOURCE_NOT_FOUND',
            message='Reset password token not found',
        )
    except ResetPasswordTokenExpired:
        return build_error_response(
            status_code=400,
            code='RESET_PASSWORD_TOKEN_EXPIRED',
            message='Reset password token expired',
        )

    return {
        'statusCode': 204,
        'body': ''
    }
