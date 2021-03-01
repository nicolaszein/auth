from auth.application.user_service import UserService
from auth.infrastructure.exception import UserNotFound
from auth.view.decorator import validate_request_body
from auth.view.resource.create_reset_password_request import CreateResetPasswordRequest


@validate_request_body(CreateResetPasswordRequest)
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
