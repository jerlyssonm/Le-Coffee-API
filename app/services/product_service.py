from os import getenv
from werkzeug.exceptions import BadRequest
import re

def validate_product(request_data: dict):
    valid_keys = set(getenv("PRODUCT_KEYS").split(","))
    valid_categories = getenv("CATEGORY_TYPES").split(",")
    valid_regions = getenv("REGIONS").split(",")
    allowed_number_of_keys_ = 7

    if len(request_data) < allowed_number_of_keys_:
        missing_keys = valid_keys - set(request_data.keys())
        error_description = {"missing keys": list(missing_keys)}

        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)[0]}

        raise BadRequest(description=error_description)

    wrong_keys = set(request_data) - valid_keys

    if wrong_keys:
        error_description = {"wrong keys": list(wrong_keys)}

        if len(wrong_keys) == 1:
            error_description = {"wrong key": list(wrong_keys)[0]}

        raise BadRequest(description=error_description)

    if request_data['category'] not in valid_categories:
        error_description = {"Invalid Category": request_data['category'], "Categories availiable": valid_categories}

        raise BadRequest(description=error_description)

    request_data['region'] = request_data['region'].title()
    
    if request_data['region'] not in valid_regions:
        error_description = {
            "Invalid Region": request_data['region'],
            "regions availiable": valid_regions
        }
    
        raise BadRequest(description=error_description)

    latitude: str = request_data["latitude"]
    match_rule_latitude = r"^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$"
    match_response_latitude = re.fullmatch(match_rule_latitude, latitude)

    if match_response_latitude is None:
        raise BadRequest({
            "error_message": "latitude is invalid",
            "valid_latitude": {
            "max_value": "+90.000",
            "min_value": "-90.00"
            },
            "invalid_latitude": latitude
        })

    longitude: str = request_data["longitude"]
    match_rule_longitude = r"^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$"
    match_response_longitude = re.fullmatch(match_rule_longitude, longitude)
    
    if match_response_longitude is None:
        raise BadRequest({
            "error_message": "longitude is invalid",
            "valid_longitude": {
                "max_value": "+180.000",
                "min_value": "-180.000"
            },
            "invalid_longitude": longitude
        })


    formatted_data = {
        'name': request_data['name'].title(),
        'price': float('{:.2f}'.format(request_data['price'])) ,
        'description': request_data['description'],
        'region': request_data['region'],
        'category': request_data['category'],
        'latitude': request_data['latitude'],
        'longitude': request_data['longitude'],
    }


    return formatted_data

def validate_update_product(request_data: dict):
    valid_keys = set(getenv("PRODUCT_KEYS").split(","))
    valid_categories = getenv("CATEGORY_TYPES").split(",")
    valid_regions = getenv("REGIONS").split(",")
    valid_values = {
        "name":"str",
        "price":"float",
        "description":"str",
        "category": "str",
        "latitude":"str",
        "longitude":"str"
    }

    wrong_keys = set(request_data) - valid_keys

    if wrong_keys:
        error_description = {
            "valid_keys": list(valid_keys),
            "wrong_keys": list(wrong_keys)
        }

        raise BadRequest(description = error_description)


    invalid_values = {}
    
    for key, value in request_data.items():
        value_type = str(type(value))[8:-2]

        if value_type != valid_values[key]:
            invalid_values[key] = value

    if invalid_values:
        error_description = {
            "valid_values": valid_values,
            "wrong_values": invalid_values
        }
        raise BadRequest(description = error_description)


    product_category = request_data.get('category')

    if product_category and product_category not in valid_categories:
        error_description = {
            "Invalid Category": request_data['category'],
            "Categories availiable": valid_categories
        }

        raise BadRequest(description = error_description)


    product_region = request_data.get('region')
    
    if product_region and product_region.title() not in valid_regions:
        request_data["name"] = product_region.title()

        error_description = {
            "Invalid Region": request_data["name"],
            "regions availiable": valid_regions
        }

        raise BadRequest(description=error_description)


    latitude: str = request_data.get("latitude")

    if latitude:
        match_rule_latitude = r"^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$"
        match_response_latitude = re.fullmatch(match_rule_latitude, latitude)

        if match_response_latitude is None:
            raise BadRequest({
                "error_message": "latitude is invalid",
                "valid_latitude": {
                "max_value": "+90.000000",
                "min_value": "-90.000000"
                },
                "invalid_latitude": latitude
            })


    longitude: str = request_data.get("longitude")

    if longitude:
        match_rule_longitude = r"^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$"
        match_response_longitude = re.fullmatch(match_rule_longitude, longitude)
        
        if match_response_longitude is None:
            raise BadRequest({
                "error_message": "longitude is invalid",
                "valid_longitude": {
                    "max_value": "+180.000000",
                    "min_value": "-180.000000"
                },
                "invalid_longitude": longitude
            })

    return request_data