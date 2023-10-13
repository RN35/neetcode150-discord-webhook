import csv
import datetime
import json
import os

import requests


def send_discord_message(webhook_url, message):
    """
    Sends a message to a Discord webhook.

    Parameters:
    webhook_url (str): The URL of the Discord webhook.
    message (str): The message to send.

    Raises:
    Exception: If there is an error sending the message.
    """

    payload = {"content": message}

    # Send the message to the Discord webhook
    response = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 204:
        raise Exception(f"Error sending message: {response.text}")

def run_thread(webhook_url, filename):
    

    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        for idx, row in enumerate(reader):

            date_str, link = row

            date_obj = datetime.datetime.strptime(date_str, "%m/%d/%y").date()

            if date_obj == datetime.date.today():
                message = f"Day {idx+1}: {link}"
                try:
                    send_discord_message(webhook_url, message)
                except Exception as e:
                    print(f"An error occurred while sending the Discord message: {e}")
                    raise e


if __name__ == "__main__":
    # Set the Discord webhook URL
    easy_webhook_url = os.environ.get("DLC_WEBHOOK_URL")
    shuffled_webhook_url = os.environ.get("DLC_WEBHOOK_URL_2")

    run_thread(easy_webhook_url, "ordered-neetcode_150_list.csv")
    run_thread(shuffled_webhook_url, "shuffled-neetcode_150_list.csv")