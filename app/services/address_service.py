import re
from os import getenv

from werkzeug.exceptions import BadRequest


def check_address_data(request_data: dict):
  valid_keys = set(getenv("ADDRESS_KEYS").split(","))
  wrong_keys = set(request_data) - valid_keys

  allowed_number_of_keys_ = 6

  if len(request_data) < allowed_number_of_keys_:
        missing_keys = valid_keys - set(request_data.keys())
        error_description = {"missing keys": list(missing_keys)}

        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)[0]}
  
  if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )

  cep: str = request_data["cep"]
  match_rule_longitude = r"^[0-9]{5}-[0-9]{3}$"
  match_response_cep = re.fullmatch(match_rule_longitude, cep)

  if match_response_cep is None:
      raise BadRequest(
          description={
              "error_message": "cep is invalid",
              "valid_cep_format": "xxxxx-xxx",
              "invalid_longitude": cep,
            }
        )

  formatted_data = {
        "street": request_data["street"].title().strip(),
        "number": request_data["number"].strip(),
        "city": request_data["city"].title().strip(),
        "state": request_data["state"].title().strip(),
        "country": request_data["country"].title().strip(),
        "cep": request_data["cep"].strip()
    }
  
  return formatted_data


def check_address_data_update(request_data: dict):
    valid_keys = set(getenv("ADDRESS_KEYS").split(","))
    wrong_keys = set(request_data) - valid_keys

    if wrong_keys:
        error_description = {"wrong keys": list(wrong_keys)}

        if len(wrong_keys) == 1:
            error_description = {"wrong key": list(wrong_keys)[0]}

        raise BadRequest(description=error_description)

    if 'cep' in request_data.keys():
      cep: str = request_data["cep"]
      match_rule_longitude = r"^[0-9]{5}-[0-9]{3}$"
      match_response_cep = re.fullmatch(match_rule_longitude, cep)

      if match_response_cep is None:
          raise BadRequest(
              description={
                  "error_message": "cep is invalid",
                  "valid_cep_format": "xxxxx-xxx",
                  "invalid_longitude": cep,
                }
            )
    
    return request_data