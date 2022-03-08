from os import getenv
from werkzeug.exceptions import BadRequest

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
        error_description = {"Invalid Region": request_data['region'], "regions availiable": valid_regions}
    

        raise BadRequest(description=error_description)

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