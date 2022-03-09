from os import getenv
from werkzeug.exceptions import BadRequest


def check_address_data(data: dict, check_missing_keys: bool = True):
  invalid_keys = []
  missing_keys = ["street", "number", "city", "state", "country", "cep"]
  invalid_values = {}
  valid_address = {"street": str, "number": str, "city": str, "state": str, "country": str, "cep": str}

  for key, value in data.items():
    if key not in valid_address:
      invalid_keys.append(key)

    if type(value) != str:
      invalid_values[key] = value

    if key in missing_keys:
      missing_keys.remove(key)

  if len(missing_keys) > 0 and check_missing_keys:
    error_description = {
      "available_keys": ["street", "number", "city", "state", "country", "cep"],
      "missing_keys": missing_keys
    }
    raise BadRequest(description=error_description)

  if len(invalid_keys) > 0:
    error_description = {
      "available_keys": ["name", "latitude", "longitude"],
      "wrong_keys": invalid_keys
    }
    raise BadRequest(description=error_description)

  if len(invalid_values) > 0:
    error_description = {
      "available_values": {"street": str, "number": str, "city": str, "state": str, "country": str, "cep": str},
      "wrong_values": invalid_values
    }
    raise BadRequest(description=error_description)

  formatted_data = {
        "street": data["street"].title(),
        "number": data["number"],
        "city": data["city"].title(),
        "state": data["state"].title(),
        "country": data["country"].title(),
        "cep": data["cep"]
    }
  
  return formatted_data


def check_address_data_update(request):
    accepted_keys = set(getenv("ADDRESS_KEYS").split(","))
    request_keys = set(request.keys())
    wrong_keys = set(request) - accepted_keys

    if wrong_keys:
        error_description = {"wrong keys": list(wrong_keys)}

        if len(wrong_keys) == 1:
            error_description = {"wrong key": list(wrong_keys)[0]}

        raise BadRequest(description=error_description)
    
    return request