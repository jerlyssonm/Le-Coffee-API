from os import getenv
import re
from werkzeug.exceptions import BadRequest


def validate_feedback(request_data: dict):
    
    valid_keys = set(getenv("FEEDBACK_KEYS").split(","))
    allowed_number_of_keys_ = 2

    if len(request_data) < allowed_number_of_keys_:
        missing_keys = valid_keys - set(request_data.keys())
        error_description = {"missing keys": list(missing_keys)}

        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)[0]}

        raise BadRequest(description=error_description)

    wrong_keys = set(request_data.keys()) - valid_keys

    if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )
    
    if not isinstance(request_data["text"], str):
        error_description = {"wrong value": request_data["text"]}
        raise BadRequest(description=error_description)

    formatted_feedback = {
        "text": request_data["text"].capitalize(),
        "rating": float(request_data["rating"])
    }
    
    return formatted_feedback


def validate_feedback_update(request_data: dict):
    
    valid_keys = set(getenv("FEEDBACK_KEYS").split(","))

    wrong_keys = set(request_data.keys()) - valid_keys

    if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )
    
    if not isinstance(request_data["text"], str):
        error_description = {"wrong value": request_data["text"]}
        raise BadRequest(description=error_description)
        
    if "text" in request_data.keys():
        request_data["text"] = request_data["text"].capitalize()

    if "rating" in request_data.keys():
        request_data["rating"] = float(request_data["rating"])

    
    return request_data