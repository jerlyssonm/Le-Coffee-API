from os import getenv
from werkzeug.exceptions import BadRequest

def check_valid_keys_order(request_data: dict):
    
    valid_keys = set(getenv("ORDER_KEYS").split(","))
    allowed_number_of_keys_ = 2

    if len(request_data) < allowed_number_of_keys_:
        missing_keys = valid_keys - set(request_data.keys())
        error_description = {"missing keys": list(missing_keys)}

        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)[0]}
            
    wrong_keys = set(request_data.keys()) - valid_keys

    if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )
    

        raise BadRequest(description=error_description)

    return request_data