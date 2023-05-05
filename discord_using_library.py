import csv
import datetime
import os

import discord

# Discord Intents
intents = discord.Intents.default()
intents.message_content = True

# Register Intents
bot = discord.Client(intents=intents)

# Channel Ids
leetcode_channel_id = int(os.environ.get("LEETCODE_CHANNEL_ID"))
solutions_channel_id = int(os.environ.get("SOLUTIONS_CHANNEL_ID"))

global_day = -1
green_prompt = "\033[92m"


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
                global global_day
                global_day = day
                return f"Day {day}: {link}"

    return ""


@bot.event
async def on_ready():
    """
    Callback function that is called when the bot has logged in and things are set up.
    Posts a message in Leetcode channel.
    """

    print(green_prompt + "Bot is ready")

    # Get today's problem from the csv file
    message = get_todays_problem()

    # Post the problem as a message in Leetcode channel
    leetcode_channel = bot.get_channel(leetcode_channel_id)
    await leetcode_channel.send(message)
    print(green_prompt + 'Posted message in the Leetcode channel')


# Listens to any 'message' events
@bot.event
async def on_message(message):
    """
    Callback function that is called when the bot has received a message.
    Checks if the message is received from the bot itself and the channel is Leetcode.
    Creates a thread in the Solutions channel and posts a starter message in the thread.
    """

    if message.author == bot.user and message.channel.id == leetcode_channel_id:
        print(green_prompt + f"Logged in as {bot.user.name}")

        thread_message = "Today's Solutions"
        if global_day != -1:
            thread_message = f"Day {global_day} Solutions"

        # Create a thread in the Solutions channel
        channel = bot.get_channel(solutions_channel_id)
        thread = await channel.create_thread(name=thread_message)
        print(green_prompt + f'Created thread: {thread.name}')

        # Post a starter message in the newly created thread
        await thread.send("Post your solutions here.")
        await channel.send(thread.jump_url)
        print(green_prompt + 'Posted message in the new thread')


if __name__ == "__main__":
    # Run the bot
    bot_token = os.environ.get("BOT_TOKEN")
    bot.run(bot_token)
