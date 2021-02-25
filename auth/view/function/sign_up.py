from auth.application.user_service import UserService
from auth.view.decorator import validate_request_body
from auth.view.resource.sign_up_request import SignUpRequest


@validate_request_body(SignUpRequest)
def handle(request, event, context):
    UserService().sign_up(
        full_name=request.full_name,
        email=request.email,
        password=request.password
    )

    response = {
        'statusCode': 204,
        'body': ''
    }

    return response
