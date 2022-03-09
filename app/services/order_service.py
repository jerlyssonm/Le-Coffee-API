from os import getenv
from werkzeug.exceptions import BadRequest

def check_valid_keys_order(request):
    accepted_keys = set(getenv("ORDER_KEYS").split(","))
    request_keys = set(request.keys())
    wrong_keys = set(request) - accepted_keys

    if len(request) < 2:
        missing_keys = accepted_keys - request_keys
        error_description = {"missing keys": list(missing_keys)}

        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)[0]}

        raise BadRequest(description=error_description)

    if wrong_keys:
        error_description = {"wrong keys": list(wrong_keys)}

        if len(wrong_keys) == 1:
            error_description = {"wrong key": list(wrong_keys)[0]}

        raise BadRequest(description=error_description)
    return request