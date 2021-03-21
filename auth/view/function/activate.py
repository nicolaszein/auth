from auth.application.user_service import UserService
from auth.domain.exception import ActivationExpired
from auth.infrastructure.exception import UserNotFound
from auth.view.decorator import validate_request_body
from auth.view.helper import build_error_response, build_success_response
from auth.view.resource.activate_request import ActivateRequest


@validate_request_body(ActivateRequest)
def handle(request, event, context):
    try:
        UserService().activate(code=request.code)
    except UserNotFound:
        return build_error_response(
            status_code=404,
            code='RESOURCE_NOT_FOUND',
            message='Activation Code not found',
        )
    except ActivationExpired:
        return build_error_response(
            status_code=400,
            code='ACTIVATION_CODE_EXPIRED',
            message='Activation Code expired',
        )

    return build_success_response(status_code=204)
