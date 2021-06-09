import os
import settings
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot


def main():
    
    client = commands.Bot(command_prefix=settings.COMMAND_PREFIX, help_command=None)
        
    @client.command()
    async def load(ctx,extension):
        client.load_extension(f'cogs.{extension}')

    @client.command()
    async def unload(ctx,extension):
        client.unload_extension(f'cogs.{extension}')

    #load all cogs at startup
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')


    client.run(settings.BOT_TOKEN)



if __name__ == "__main__":
    main()