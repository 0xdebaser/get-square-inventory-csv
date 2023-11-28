import os
from square.client import Client


def get_catalog_objects(token, target_location):
    """
    Returns a list of all item variation ids with stock at the target location.
    See https://developer.squareup.com/reference/square/catalog-api/list-catalog
    for more info.
    """
    client = Client(access_token=token, environment="production")
    cursor = "initial request"

    # Currently the Square API limits results to 100 per page; therefore, results are limited to 100x this variable.
    # This variable should be set to safely exceed the number of catalog items expected, as it is primarily designed as
    # a fail-safe against an infinite loop.
    counter_limit = 100
    counter = 1

    item_variations_list = []
    while cursor is not None and counter <= counter_limit:
        print(f"Starting get_catalog_objects API call #{counter}...")
        if cursor == "initial request":
            cursor = None
        result = client.catalog.list_catalog(
            types="ITEM_VARIATION", cursor=cursor)
        if result.is_success():
            objects = result.body.get("objects")
            cursor = result.body.get("cursor")
            for object in objects:
                if object.get("present_at_location_ids") is not None and target_location in object.get("present_at_location_ids"):
                    variation_data = object.get("item_variation_data")
                    if variation_data.get("price_money") is not None:
                        price = variation_data.get(
                            "price_money").get("amount") / 100
                    else:
                        price = None
                    new_obj = {
                        "Token": object.get("id"),
                        "SKU": variation_data.get("sku"),
                        "GTIN": variation_data.get("upc"),
                        "Price": price
                    }
                    item_variations_list.append(new_obj)
        elif result.is_error():
            print(result.errors)
            break
        counter += 1
    return item_variations_list
