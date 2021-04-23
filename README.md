# Discord Ban Bot

This bot facilitates banning many users at a time on Discord using regular expressions.

## Requirements

### Software & Libraries

* python3
* [discord.py](https://discordpy.readthedocs.io/en/stable/), [python-dateutil](https://dateutil.readthedocs.io/en/stable/)
  ```bash
  python3 -m pip install -U discord.py python-dateutil
  ```
  
### Create a Discord bot token

1. Create an application: https://discord.com/developers/applications .
2. Enable the bot in the tab "Bot" on the side.
3. Disable "Public Bot".
4. Enable "Server Members Intent".
5. Copy the token and set the environment variable in your terminal `export DISCORD_BAN_BOT_TOKEN=thetoken`.   
6. Go to the tab "OAuth2" and check "bot" followed by "Kick Members", "Ban Members", "View Channels".
7. Copy the URL, go to the URL, and join the server you want to ban people from.

## Use

```bash
python3 ban.py --after 2021-04-23 'botToBanUser.*'
```

The bot will let you confirm before actually banning the users.

