import os
from square.client import Client


def get_inventory_counts(token, target_location, item_variations_list):
    """
    Adds inventory counts for a specified location to paramater item_variations_list.
    See https://developer.squareup.com/reference/square/inventory-api/batch-retrieve-inventory-counts
    for more info.
    """
    client = Client(access_token=token, environment="production")
    item_variation_ids_list = [
        item_variation.get("Token") for item_variation in item_variations_list]
    counts_by_id_dict = {}

    # Break item_variation_ids_list into sub-lists of <= 100 to meet Square limits
    ids = []
    sub_lists_needed = - \
        (len(item_variation_ids_list) // -100)  # ceiling dvision
    for i in range(sub_lists_needed):
        if i == sub_lists_needed - 1:
            ids.append(item_variation_ids_list[100 * i:])
        else:
            ids.append(item_variation_ids_list[100 * i: 100 * (i + 1)])
    print(len(ids))

    for sub_list_num, sub_list in enumerate(ids):
        counter_limit = 3
        counter = 1
        cursor = "initial request"

        while cursor is not None and counter <= counter_limit:
            print(
                f"Starting get_inventory_counts API call #{sub_list_num}-{counter}...")
            if cursor == "initial request":
                cursor = None
            result = client.inventory.batch_retrieve_inventory_counts(
                body={
                    "catalog_object_ids": sub_list,
                    "location_ids": [target_location],
                    "states": ["IN_STOCK"],
                    "cursor": cursor
                })
            if result.is_success():
                counts = result.body.get("counts")
                cursor = result.body.get("cursor")
                if counts is not None:
                    for count in counts:
                        count_id = count.get("catalog_object_id")
                        count_quantity = count.get("quantity")
                        if count_id in counts_by_id_dict:
                            print(f"Duplicate count detected for {count_id}!")
                        counts_by_id_dict[count_id] = count_quantity
            elif result.is_error():
                print(result.errors)
                break
            counter += 1

    # Incorporate inventory counts into exisiting item_variations_list
    for item in item_variations_list:
        quantity = counts_by_id_dict.get(item["Token"])
        item["Quantity"] = quantity

    return item_variations_list
