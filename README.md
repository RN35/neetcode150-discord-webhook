# neetcode150-discord-webhook

This can be used to post [Neetcode 150](https://neetcode.io/practice) questions as daily challenges on a Discord channel. 
</br>

Built with:
- [Discord Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
- Uses Github Actions for cron scheduling

> :warning: **The worflow might not trigger**: The schedule event can be delayed during periods of high loads of GitHub Actions workflow runs. 
> High load times include the start of every hour. If the load is sufficiently high enough, some queued jobs may be dropped. 
> To decrease the chance of delay, schedule your workflow to run at a different time of the hour.
Reference: [Github Actions Docs](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
