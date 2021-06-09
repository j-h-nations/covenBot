import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self,client):
        self.client = client

        self.guild = self.client.get_guild(714939391889375274)
        
        ###HELP EMBED###
        self.Embed=discord.Embed(title="**A wild familiar appeared**", description="Listed below are the various help commands", color=0x2dc3d7)
        self.Embed.set_author(name="CovenBot")
        self.Embed.add_field(name="Economy", value="`.econHelp`", inline=True)
        self.Embed.add_field(name="Events", value="`.eventHelp`", inline=True)   
        self.Embed.add_field(name="Admin", value="`.adminHelp`", inline=True)     
        ###ADMIN EMBED###
        self.adminEmbed=discord.Embed(title="Admin Help", description="Bot Version 0.1", color=0x2dc3d7)
        self.adminEmbed.set_author(name="CovenBot")
        self.adminEmbed.add_field(name="Load Cog", value="`.load <name of cog>`", inline=True)
        self.adminEmbed.add_field(name="Unload Cog", value="`.unload <name of cog>`", inline=True)
        self.adminEmbed.add_field(name="Start Event Channel", value="`.startEventChann`")
        ###ECONOMY EMBED###
        self.econEmbed = discord.Embed(title = "Economy Help (UNDER CONSTRUCTION)", description= "Commands related to economy", color=0x40a832)
        self.econEmbed.set_author(name="CovenBot")
        self.econEmbed.add_field(name="Open Account",value="`.openAcc`", inline=True) 
        ###EVENT EMBED###
        self.eventEmbed = discord.Embed(title = "Events Help (UNDER CONSTRUCTION)", description= "Commands related to events. Must be level 15 or above to host", color=0xb86ea9)
        self.eventEmbed.set_author(name="CovenBot")
        self.eventEmbed.add_field(name="Host Event",value="`.host`", inline=True) 

    @commands.Cog.listener()
    async def on_ready(self):
        
        print('Bot Online')
        print(discord.__version__)
        
        guild = self.client.get_guild(714939391889375274)

        # TO-DO: Create a utils function to search for any text channel by attribute
        checkStart = True
        for channels in guild.text_channels:
            if str(channels) == 'bot-setup':
                checkStart = False

        if checkStart == True:        
            channel = await guild.create_text_channel('Bot-Setup')
            await channel.send(embed=self.adminEmbed)


    @commands.command()
    async def help(self,ctx):
        await ctx.send(embed=self.Embed)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def adminHelp(self,ctx):
        await ctx.send(embed=self.adminEmbed)
    
    @commands.command()
    async def econHelp(self,ctx):
        await ctx.send(embed=self.econEmbed)
    
    @commands.command()
    async def eventHelp(self,ctx):
        await ctx.send(embed=self.eventEmbed)

    @commands.has_permissions(manage_guild = True)
    async def startEventChann(self,ctx):
        guild = self.client.get_guild(714939391889375274)
        channel2 = await guild.create_text_channel('Event Organization')
        await ctx.send("Event Organization Channel Created")

    
def setup(client):
    client.add_cog(help(client))