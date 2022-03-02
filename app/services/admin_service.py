from os import getenv
from werkzeug.exceptions import BadRequest

def validate_admin(request_data: dict):
    valid_keys = set(getenv('ADM_KEYS').split(","))
    wrong_keys = set(request_data.keys()) - valid_keys
    wrong_values_type = [ value for value in request_data.values() if type(value) != str ]

    if len(request_data) < 3:
        missing_keys = valid_keys - set(request_data.keys())
        error_description = {"missing keys": list(missing_keys)}

        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)[0]}

        raise BadRequest(description=error_description)

    if wrong_keys:
        error_description = {"wrong keys": list(wrong_keys)}

        if len(wrong_keys) == 1:
            error_description = {"wrong key": list(wrong_keys)[0]}

        raise BadRequest(description=error_description)

    if wrong_values_type:
        raise BadRequest(
            description={"error_message": "All field values must be a string type"}
        )

    return request_data