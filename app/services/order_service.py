from os import getenv

from werkzeug.exceptions import BadRequest


def check_valid_keys_order(request_data: dict):
    
    valid_keys = set(getenv("ORDER_KEYS").split(","))
    allowed_number_of_keys_ = 2
    validated_data = {
        "status": False,
        "cart_products":[
            {
                "product_id": request_data["product_id"],
                "quantity": request_data["quantity"]
            }
        ]
    }

    if len(validated_data["cart_products"]) < allowed_number_of_keys_:
        missing_keys = valid_keys - set(validated_data["cart_products"][0])
        error_description = {"missing keys": list(missing_keys)}


        if len(missing_keys) == 1:
            error_description = {"missing key": list(missing_keys)["cart_products"]}
            
            raise BadRequest(description=error_description)
    wrong_keys = set(validated_data["cart_products"][0].keys()) - valid_keys

    if wrong_keys:
        raise BadRequest(
            description={
                "available_keys": list(valid_keys),
                "wrong_keys": list(wrong_keys),
            }
        )


    return validated_data