from psycopg2.errors import NotNullViolation

def check_region_data(data: dict, check_missing_keys: bool = True):
  """
    Check keys and values to create a new region.
    This function receive the data to check and optional paramn check_missing_keys that by default is True
    \n
    If check_missing_keys is True this function will check missing_keys
    \n
    Raise an Error if something do not satisfy the conditions
  """

  invalid_keys = []
  missing_keys = ["name", "latitude", "longitude"]
  invalid_values = {}
  valid_region = {"name": str, "latitude": str, "longitude": str}

  for key, value in data.items():
    if key not in valid_region:
      invalid_keys.append(key)

    if type(value) != str:
      invalid_values[key] = value

    if key in missing_keys:
      missing_keys.remove(key)

  if len(missing_keys) > 0 and check_missing_keys:
    error = {
      "available_keys": ["name", "latitude", "longitude"],
      "missing_keys": missing_keys
    }
    raise NotNullViolation(error)

  if len(invalid_keys) > 0:
    error = {
      "available_keys": ["name", "latitude", "longitude"],
      "wrong_keys": invalid_keys
    }
    raise KeyError(error)

  if len(invalid_values) > 0:
    error = {
      "available_values": {"name": "str", "latitude": "str", "longitude": "str"},
      "wrong_values": invalid_values
    }
    raise ValueError(error)

  name = data["name"]
  data["name"] = name.title()
  
  return data