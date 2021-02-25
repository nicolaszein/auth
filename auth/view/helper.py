import json


def build_error_response(status_code, code, message, details=None):
    body = {
        'code': code,
        'message': message,
    }
    if details:
        body['details'] = details

    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }


def build_input_error_response(errors):
    details = [dict(target=error['loc'][0], message=error['msg']) for error in errors]

    return build_error_response(
        status_code=400,
        code='INPUT_VALIDATION_ERROR',
        message='Some fields are not valid',
        details=details
    )
