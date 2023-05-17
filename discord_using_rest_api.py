import csv
import datetime
import json
import os

import requests

green_prompt = "\033[92m"
base_url = "https://discord.com/api"


def send_request(path, headers, data, success_status, error_message):
    """
    Sends a POST request to discord

    Parameters:
    ------------
    path: type: str
        The API path for the request

    Raises:
    -----------
    requests.RequestException
        Creating a thread failed

    Returns:
    -----------
    :type: requests.Response
    Returns the response object
    """

    response = requests.post(base_url + path, headers=headers, data=data)

    if response.status_code != success_status:
        raise requests.RequestException(error_message + response.text)
    return response


def get_todays_problem():
    """
    Fetches today's problem from the csv file.
    Uses today's date as a key to match the record in csv file.

    Returns:
    -----------
    Tuple[:type: int, :type: str]
    A tuple of elapsed days and problem link
    """

    with open("neetcode_150_list.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        for idx, row in enumerate(reader):
            day, date_str, link = row
            date_obj = datetime.datetime.strptime(date_str, "%m/%d/%y").date()

            if date_obj == datetime.date.today():
                return day, f"Day {day}: {link}"

    return ""


class DiscordBot:
    def __init__(self):
        self.__leetcode_channel_id = int(os.environ.get("LEETCODE_CHANNEL_ID"))
        self.__solutions_channel_id = int(os.environ.get("SOLUTIONS_CHANNEL_ID"))
        self.__bot_token = os.environ.get("BOT_TOKEN")

        if self.__leetcode_channel_id is None:
            raise Exception("ERROR: Unable to extract leetcode channel id")
        if self.__solutions_channel_id is None:
            raise Exception("ERROR: Unable to extract solutions channel id")
        if self.__bot_token is None:
            raise Exception("ERROR: Unable to extract bot token")

        self.__headers = {"Authorization": "Bot {}".format(self.__bot_token),
                          "Content-Type": "application/json"
                          }

    def __post_message_in_thread(self, thread_response):
        """
        Posts a message in the newly created thread to get things started

        Parameters:
        ------------
        thread_response: type: requests.Response
            Thread response from creating thread

        Returns:
        -----------
        None
        """

        thread_id = json.loads(thread_response.text)['id']
        data = json.dumps({"content": "Post your solutions here."})
        send_request(
            "/channels/{}/messages".format(thread_id),
            self.__headers,
            data,
            200,
            "Error posting a message in new thread\n"
        )
        print(green_prompt + "SUCCESS: Posted message in the new thread")

    def __create_thread(self, day):
        """
        Creates a thread in solutions channel

        Parameters:
        ------------
        day: type: int
            Elapsed days

        Returns:
        -----------
        None
        """
        data = json.dumps({"name": f"Day {day} Solutions", "type": 11, "message": "Post your solutions here"})
        thread_response = send_request(
            "/channels/{}/threads".format(self.__solutions_channel_id),
            self.__headers,
            data,
            200,
            "Error creating a thread in solutions channel\n"
        )
        print(green_prompt + "SUCCESS: Created a thread in Solutions channel")
        self.__post_message_in_thread(thread_response)

    def __post_message_in_channel(self):
        """
        Posts a message in Leetcode channel

        Returns:
        -----------
        None
        """

        day, message = get_todays_problem()
        if message == "":
            raise Exception("ERROR: Unable to fetch data from csv file")

        # Post today's problem to Leetcode channel
        data = json.dumps({"content": message})
        send_request(
            "/channels/{}/messages".format(self.__leetcode_channel_id),
            self.__headers,
            data,
            200,
            "Error posting a message in leetcode channel\n"
        )
        print(green_prompt + "SUCCESS: Posted message to Leetcode channel")
        self.__create_thread(day)

    def run(self):
        """
        As the name suggests, run() gets things started
        """

        self.__post_message_in_channel()


if __name__ == "__main__":
    discord_bot = DiscordBot()
    discord_bot.run()
