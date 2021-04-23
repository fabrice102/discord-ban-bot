#!/usr/bin/env python3

import argparse
import datetime
import os
import re
import sys

import dateutil.parser
import discord

# Maximum numbers of members to list
limit_members=1000


def full_name(member: discord.Member):
    return f"{member.name}#{member.discriminator}"


class MyClient(discord.Client):
    def __init__(self, after: datetime.datetime, users: list[re.Pattern]):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)

        self.filter_after = after
        self.filter_users = users

    async def on_ready(self):
        print(f"Logged on as {self.user}")
        members_to_ban = []
        for guild in self.guilds:
            async for member in guild.fetch_members(limit=limit_members):
                if any(
                        u.match(member.name) or
                        u.match(full_name(member)) or
                        u.match(member.display_name)
                        for u in self.filter_users
                ):
                    members_to_ban.append(member)

        print(f"Found {len(members_to_ban)} users to ban:")
        for m in members_to_ban:
            print(f"   {full_name(m)} ({m.display_name})")

        print()
        print(f"Are you sure you want to ban these {len(members_to_ban)} users? (yes/NO)")

        s = input()
        if s.lower() == "yes":
            print("Banning:")
            for m in members_to_ban:
                await m.ban()
                print(f"   {full_name(m)} ({m.display_name})\t\t-> banned")
        else:
            print("Aborting. You need to write 'yes' to continue.")

        await self.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--after", type=dateutil.parser.parse, required=True,
                        help="only consider users after this date")
    parser.add_argument("users", nargs="+",
                        help="regexp for the users to ban")
    args = parser.parse_args()

    token = os.getenv("DISCORD_BAN_BOT_TOKEN")
    if not token:
        print("Missing environment variable DISCORD_BAN_BOT_TOKEN", file=sys.stderr)
        sys.exit(1)

    users = [re.compile(u) for u in args.users]
    after = args.after

    print(f"Trying to ban users after: {after.isoformat()} matching:")
    for u in args.users:
        print(f"  - {u}")
    print()

    client = MyClient(after, users)
    client.run(token)


if __name__ == "__main__":
    main()
