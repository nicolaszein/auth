from auth.application.user_service import UserService
from auth.infrastructure.exception import UserNotFound
from auth.view.decorator import validate_request_body
from auth.view.resource.reset_password_request import ResetPasswordRequest


@validate_request_body(ResetPasswordRequest)
def handle(request, event, context):
    try:
        UserService().create_reset_password_token(email=request.email)
    except UserNotFound:
        pass

    response = {
        'statusCode': 204,
        'body': ''
    }

    return response
