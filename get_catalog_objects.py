from square.core.api_error import ApiError
import time

def get_catalog_objects(token, target_location, client):
    """
    Returns a list of all item variation ids with stock at the target location.
    See https://developer.squareup.com/reference/square/catalog-api/list-catalog
    for more info.
    """
    # cursor = "initial request"

    # # Currently the Square API limits results to 100 per page; therefore, results are limited to 100x this variable.
    # # This variable should be set to safely exceed the number of catalog items expected, as it is primarily designed as
    # # a fail-safe against an infinite loop.
    # counter_limit = 100
    # counter = 1

    start_time = time.time()

    item_variations_list = []
    try:
        response = client.catalog.list(types="ITEM_VARIATION")
        for object in response:
            present_at_location_ids = object.present_at_location_ids
            if present_at_location_ids is not None and target_location in present_at_location_ids:
                variation_data = object.item_variation_data
                price_money = variation_data.price_money
                price = price_money.amount / 100 if price_money else None
                new_obj = {
                    "Token": object.id,
                    "SKU": variation_data.sku,
                    "GTIN": variation_data.upc,
                    "Price": price,
                }
                item_variations_list.append(new_obj)
    
    except ApiError as e:
        for error in e.errors:
            print(error.category)
            print(error.code)
            print(error.detail)
     
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"get_catalog_objects took {elapsed_time:.2f} seconds to complete.")
    
    return item_variations_list
