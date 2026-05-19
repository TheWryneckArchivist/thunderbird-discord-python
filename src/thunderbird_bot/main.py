import os
import re

import discord
from discord.ext import commands

from thunderbird_bot.grpc_client import ThunderbirdGrpcClient


def build_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    grpc_client = ThunderbirdGrpcClient(
        endpoint=os.getenv("GRPC_ENDPOINT", "localhost:5001")
    )

    @bot.event
    async def on_ready() -> None:
        print(f"Connected as {bot.user}")

    @bot.command(name="session_create")
    async def session_create(ctx: commands.Context, *, title: str) -> None:
        result = await grpc_client.create_session(
            host_user_id=str(ctx.author.id),
            title=title,
            ruleset_version="v1",
        )
        await ctx.send(f"Session created: {result['session_id']} ({result['title']})")

    @bot.command(name="session_join")
    async def session_join(ctx: commands.Context, session_id: str) -> None:
        result = await grpc_client.join_session(
            session_id=session_id, user_id=str(ctx.author.id)
        )
        await ctx.send(f"Join status: {result['status']} for {result['session_id']}")

    return bot


def extract_tokens(file_path) -> str:
    # Regex pattern matching the standard Discord token format
    token_pattern = re.compile(r"[A-Za-z0-9]{24}\.[A-Za-z0-9]{6}\.[A-Za-z0-9_\-]{27}")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    found_tokens = token_pattern.findall(content)
    return found_tokens.__str__()


def main() -> None:
    token = os.getenv("DISCORD_TOKEN", extract_tokens("secrets.txt"))
    if not token:
        raise RuntimeError("DISCORD_TOKEN is required")

    bot = build_bot()
    bot.run(token)


if __name__ == "__main__":
    main()
