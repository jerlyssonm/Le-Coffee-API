from os import getenv
from werkzeug.exceptions import BadRequest


def validate_request(request_data: dict, type_login: bool = False):
    valid_keys = valid_keys = set(getenv("REGISTER_KEYS").split(","))
    allowed_number_of_keys_ = 3 

    if type_login:
        valid_keys = set(getenv("LOGIN_KEYS").split(","))
        allowed_number_of_keys_ = 2

    if len(request_data) < allowed_number_of_keys_:
        missing_keys = valid_keys - set(request_data.keys())
        error_description = {"missing keys": list(missing_keys)}

        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)[0]}

        raise BadRequest(description=error_description)

    wrong_keys = set(request_data.keys()) - valid_keys

    if wrong_keys:
        error_description = {"wrong keys": list(wrong_keys)}

        if len(wrong_keys) == 1:
            error_description = {"wrong key": list(wrong_keys)[0]}

        raise BadRequest(description=error_description)

    wrong_values_type = [value for value in request_data.values() if type(value) != str]

    if wrong_values_type:
        raise BadRequest(
            description={"error_message": "All field values must be a string type"}
        )

    if 'name' in request_data.keys():
        request_data['name'] = request_data['name'].title()

    return request_data
