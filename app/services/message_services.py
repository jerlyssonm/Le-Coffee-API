from os import getenv
from werkzeug.exceptions import BadRequest

def validade_message(data: dict):
    valid_keys = set(["text", "order_id"])
    wrong_keys = set(data) - valid_keys
    missing_keys = valid_keys - set(data.keys())

    if len(missing_keys) >= 1:
        error_description = {"missing key": missing_keys}
        raise BadRequest(description=error_description)

    if len(wrong_keys) >=1:
        error_description = {"wrong keys": wrong_keys}
        raise BadRequest(description=error_description)

    if not isinstance(data["text"], str):
        raise BadRequest(description={
            "wrong value": 'text key must be string type'
        })

    if not isinstance(data["order_id"], int):
        raise BadRequest(description={
            "wrong value": 'order_id key must be integer type'
        })
    
   

    
        

