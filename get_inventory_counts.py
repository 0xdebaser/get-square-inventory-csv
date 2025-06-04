from square.core.api_error import ApiError
import time

def get_inventory_counts(token, target_location, item_variations_list, client):
    """
    Adds inventory counts for a specified location to paramater item_variations_list.
    See https://developer.squareup.com/reference/square/inventory-api/batch-retrieve-inventory-counts
    for more info.
    """

    start_time = time.time()
    
    item_variation_ids_list = [
        item_variation.get("Token") for item_variation in item_variations_list if item_variation.get("Token") is not None
    ]
    counts_by_id_dict = {}

    # Break item_variation_ids_list into sub-lists of <= 1000 to meet Square limits
    ids = []
    sub_lists_needed = -(len(item_variation_ids_list) // -1000)  # ceiling dvision
    for i in range(sub_lists_needed):
        if i == sub_lists_needed - 1:
            ids.append(item_variation_ids_list[1000 * i:])
        else:
            ids.append(item_variation_ids_list[1000 * i: 1000 * (i + 1)])
    
    # Batch retrieve inventory counts for each sub-list
    for sub_list in ids:
        try:
            response = client.inventory.batch_get_counts(
                location_ids = [target_location],
                catalog_object_ids = sub_list,
                states = ["IN_STOCK"]
            )
            for count in response:
                count_id = count.catalog_object_id
                count_quantity = count.quantity
                if count_id in counts_by_id_dict:
                    print(f"Duplicate count detected for {count_id}!")
                counts_by_id_dict[count_id] = count_quantity

        except ApiError as e:
            for error in e.errors:
                print(error.category)
                print(error.code)
                print(error.detail) 

    # Incorporate inventory counts into exisiting item_variations_list
    for item in item_variations_list:
        quantity = counts_by_id_dict.get(item["Token"], 0)
        item["Quantity"] = quantity

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"get_inventory_counts took {elapsed_time:.2f} seconds to complete.")

    return item_variations_list
