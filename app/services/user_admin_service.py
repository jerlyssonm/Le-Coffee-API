from os import getenv
from werkzeug.exceptions import BadRequest

def check_request_update(request_data: dict):
    valid_keys = set(getenv("REGISTER_KEYS").split(","))
    wrong_keys = set(request_data) - valid_keys

    if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )
    
    if 'name' in request_data.keys():
        request_data['name'] = request_data['name'].title()
    
    return request_data