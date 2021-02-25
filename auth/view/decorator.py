import json
from functools import wraps

from pydantic import ValidationError

from auth.view.helper import build_error_response, build_input_error_response


def validate_request_body(schema):
    def wrapper(function):
        @wraps(function)
        def wrapped(event, context, *args, **kwargs):
            try:
                body = json.loads(event.get("body") or "{}")
            except ValueError:
                return build_error_response(
                    status_code=400,
                    code='BAD_REQUEST',
                    message='Invalid request body'
                )

            try:
                request = schema(**body)
            except ValidationError as e:
                return build_input_error_response(e.errors())

            return function(request, event, context, *args, **kwargs)

        return wrapped

    return wrapper
