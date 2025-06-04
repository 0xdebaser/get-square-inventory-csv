import csv

filename = "inventory_data_for_locally.csv"


def write_to_csv(item_variations_list):
    """
    Writes the contents of parameter item_variations_list to a csv file.
    """
    header_row = list(item_variations_list[0].keys())
    data = list()
    for variation in item_variations_list:
        variation_data = (variation.get("Token"), variation.get("SKU"), variation.get(
            "GTIN"), variation.get("Price"), variation.get("Quantity"))
        data.append(variation_data)

    try:
        with open(filename, "wt") as fp:
            writer = csv.writer(fp, delimiter=",")
            writer.writerow(header_row)
            writer.writerows(data)
        return filename
    except:
        return False
