"""
Retrieve information from the Square API required to build the same inventory
CSV file that is downloaded from the Square Retail dashboard, then build and
save the CSV file
"""

import datetime
import os
import time
from dotenv import load_dotenv
from get_catalog_objects import get_catalog_objects
from get_inventory_counts import get_inventory_counts
from send_file_via_ftp import send_file_via_ftp
from write_to_csv import write_to_csv

load_dotenv()
token = os.getenv("SQUARE_ACCESS_TOKEN")
target_location = os.getenv("TARGET_LOCATION_ID")
server_address = os.getenv("FTP_SERVER_ADDRESS")
username = os.getenv("FTP_USERNAME")
password = os.getenv("FTP_PASSWORD")


def main():
    """
    Updates and uploads inventory immediately upon being run, then once per hour between the hours of 10:00 and 19:00. 
    """
    def update(now):
        print(f"Update started at {now}.")
        item_variations_list = get_catalog_objects(
            token=token, target_location=target_location)
        item_variations_list = get_inventory_counts(
            token=token, target_location=target_location, item_variations_list=item_variations_list)
        filename = write_to_csv(item_variations_list=item_variations_list)
        if filename:
            send_file_via_ftp(filename=filename, server_address=server_address,
                              username=username, password=password)
        else:
            print("There was an error writing data to CSV file. No data was transmitted.")
    now = datetime.datetime.now()
    update(now)
    while True:
        time.sleep(60 * 60)  # sleep for one hour
        now = datetime.datetime.now()
        current_hour = now.time().hour
        if 19 > current_hour > 9:
            update(now)
    return


if __name__ == "__main__":
    main()
