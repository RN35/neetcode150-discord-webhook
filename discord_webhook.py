import csv
import datetime
import json
import os

import requests

# Set the Discord webhook URL
webhook_url = os.environ.get("DLC_WEBHOOK_URL")

# Load the CSV file
with open("neetcode_150_list.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)

    # Skip the header row
    next(reader)

    # Loop through the rows in the CSV file
    for idx, row in enumerate(reader):

        # Get the date and link from the current row
        date_str, link = row

        # Convert the date string to a datetime object
        date_obj = datetime.datetime.strptime(date_str, "%m/%d/%y").date()

        # Check if the date matches today's date
        if date_obj == datetime.date.today():

            # Create the message payload for the Discord webhook
            payload = {"content": f"Day {idx+1}: {link}"}

            # Send the message to the Discord webhook
            response = requests.post(
                webhook_url,  # type: ignore
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
            )

            # Check if the message was sent successfully
            if response.status_code != 204:
                raise Exception(f"Error sending message: {response.text}")
