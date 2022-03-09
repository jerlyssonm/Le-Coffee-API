from os import getenv
from werkzeug.exceptions import BadRequest

def check_request_update(request):
    accepted_keys = set(getenv("REGISTER_KEYS").split(","))
    request_keys = set(request.keys())
    wrong_keys = set(request) - accepted_keys

    if wrong_keys:
        error_description = {"wrong keys": list(wrong_keys)}

        if len(wrong_keys) == 1:
            error_description = {"wrong key": list(wrong_keys)[0]}

        raise BadRequest(description=error_description)
    
    return request