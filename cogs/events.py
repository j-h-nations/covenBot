import discord
from discord.ext import commands, tasks
from datetime import datetime
import mysql.connector

class events(commands.Cog):
    def __init__(self,client):
        self.client = client

        self.guild = self.client.get_guild(714939391889375274)
        self.checkDB.start()

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="!Ziggyisblind123",
            database="covenEco",
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.db.cursor()
        self.checkCursor = self.db.cursor(buffered=True)

        ###EVENT CREATION EMBED###
        self.createEmbed = discord.Embed(title="Event Creation", description="Create an event by typing in: `.event` \nI will ask you sequentially to input the event information \nNOTE: \nInput of a month is: Jun Feb Mar... \nInput of day is: 01, 02, .. ,10, 11 \nInput of year is last 2 digits of year", color=0x2dc3d7)
        self.createEmbed.set_author(name="CovenBot")
        self.createEmbed.add_field(name="Example of a **Start Date**", value="`Jul 10 21 1:33PM`", inline=True)
        self.createEmbed.add_field(name="Example of a **End Date**", value="`Jul 10 21 1:44PM`", inline=True)
        self.createEmbed.add_field(name="Event Type(s)", value="movie, other", inline = False)

        ###EVENT CREATION EMBED###



    #Level 15 based Permision
    @commands.command()
    #@commands.has_role(597103734949937202)
    async def host(self,ctx):
        await ctx.send(embed=self.createEmbed)
    
    @tasks.loop(seconds = 10.0)
    async def checkDB(self):
        #purpose is to check table of "EVENTS" and see if the event has ended and/or already passed
        self.checkCursor.execute("SELECT id,endTime FROM Events WHERE held = 0 ORDER BY id ASC")
        for x in self.checkCursor:
            y = list(x)
            if y[1] < datetime.now():
                self.checkCursor.execute("UPDATE Events SET held = 1 WHERE id = {}".format(y[0]))
                self.db.commit()
        
    @commands.command()
    #@commands.has_role(597103734949937202)
    async def event(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            await ctx.send("When does the event start?")
            sDate = await self.client.wait_for('message', check=check, timeout=180)
            con1 = datetime.strptime(sDate.content, '%b %d %y %I:%M%p')
            if(con1 < datetime.now()):
               raise ValueError

            await ctx.send("When does the event end?")
            eDate = await self.client.wait_for('message', check=check, timeout=180)
            con2 = datetime.strptime(eDate.content, '%b %d %y %I:%M%p')
            if (con2 < datetime.now() or con2 < con1):
               raise ValueError

            await ctx.send("Choose the event Type")
            eventType = await self.client.wait_for('message', check=check, timeout=180)

        except TimeoutError:
            await ctx.send("Request Timed Out.")
        except ValueError:
            await ctx.send("Format of time was incorrect. \nOr you are trying to create an event in the past. \nPlease try again by typing `.event`")
        else:
            #If Date time was created succesfully, it will print out the bottom statement
            await ctx.send("Event Created!")

            #MYSQL CODE - ADDING EVENT TO TABLE
            self.cursor.execute("INSERT INTO Events (startTime, endTime, type, author, held) VALUES (%s,%s,%s,%s,%s)", (con1,con2,eventType.content,sDate.author.name,False))
            self.db.commit()

        
    #@event.error
    #async def event_error(self,ctx,error):
        #if isinstance(error, commands.CommandInvokeError):
            #await ctx.send("Something went horriably wrong, event was not created. Please complain to my caretaker")



def setup(client):
    client.add_cog(events(client))