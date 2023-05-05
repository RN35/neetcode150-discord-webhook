# neetcode150-discord-webhook

This can be used to post [Neetcode 150](https://neetcode.io/practice) questions as daily challenges on a Discord
channel.
</br>

Built with:

- [Discord REST API](https://discord.com/developers/docs/getting-started)
- [Discord Python Linrary](https://discordpy.readthedocs.io/en/stable/)
- Uses Github Actions for cron scheduling

Follow these steps to setup a bot and integrate it with a channel:

- Login to discord’s developer portal with discord
  credentials [Developer Portal](https://discord.com/developers/docs/intro)
- Follow the instructions on the portal to create a new application
- After creating the application, select the application. Go to the 'OAuth' section
- Select all the permission required by the bot. Save
- Next, go to the 'Bot' section and reset the token. Copy and store the token in a secure location. The bot needs this
  token to interact with the server
- Go back to 'OAuth' -> 'URL generator'. Select application.commands and bot from the list. Copy the generated URL
  below.
- Paste the URL in a new browser window. This will take you to a login/register screen. Select the server and verify the
  permissions once more.
- Open your server and see if the bot has been added as a user.

> :warning: **The worflow might not trigger**: The schedule event can be delayed during periods of high loads of GitHub
> Actions workflow runs.
> High load times include the start of every hour. If the load is sufficiently high enough, some queued jobs may be
> dropped.
> To decrease the chance of delay, schedule your workflow to run at a different time of the hour.
>
Reference: [Github Actions Docs](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
