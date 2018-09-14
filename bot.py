 
#Locally: CMD ->pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip
#Declare dependents on Heroku: git+https://github.com/Rapptz/discord.py@rewrite
#git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]

import datetime
from datetime import time
from datetime import datetime
from datetime import timedelta
import asyncio 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os 
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Get token from heroku config'd var 
bot_token = os.environ['BOT_TOKEN']

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#on_ready() called when the client is done preparing data received from Discord
#usually after bot's login is successful
#===============================================================================
#Bot functions to invoke commands
#ctx = context

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="BleeBot", description="Because math is hard.", color=0xeee657)
    embed.add_field(name="Author", value="bleeinyourself")
    embed.add_field(name="Server Count", value=f"{len(bot.guilds)}")
    embed.add_field(name="Add me to your server:", value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=469366032176381952&scope=bot)")
    await ctx.send(embed=embed)

#bot.remove_command('help')

@bot.command()
async def guide(ctx):
    embed = discord.Embed(title="List of commands:")
    embed.add_field(name="-guide", value="Gives this message", inline=False)
    embed.add_field(name="-info", value="Gives info about this bot, including an invite link", inline=False)
    embed.add_field(name="-tip", value="Calculates your tip.  Ex) -tip 20.00 18", inline=False)
    embed.add_field(name="-hatchesin", value="Gives the hatch time and despawn time given minutes left until hatch.  Ex) -hatchesin 45", inline=False)
    embed.add_field(name="-hatchesat", value="Gives the despawn time given the hatch time.  Ex) -hatchesat 09:30am", inline=False)
    embed.add_field(name="-timeleft", value="Gives the despawn time given minutes left until despawn.  Ex) -timeleft 45", inline=False)
    embed.add_field(name="-sheet", value="Gives the google sheets with stops, quests, and map links.", inline=False)
    embed.add_field(name="-report", value="Report quests from Pokestops as follows: -report stop, location, quest notes  Ex) -report ", inline=False)
    await ctx.send(embed=embed)
  
@bot.command()
async def add(ctx, a: float, b: float):
    await ctx.send(a+b)

@bot.command()
async def multiply(ctx, a: float, b: float):
    await ctx.send(a*b)

@bot.command()
async def tip(ctx, a: float, b: float):
    c = a*b/100
    await ctx.send("A {}% tip for a ${} meal or service would be: ${}".format(round(b,2), round(a,2), round(c,2)))
   
#http://www.fileformat.info/info/emoji/list.htm
@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hi.  I am Bleebot.")

#Despawn from minutes until hatch ======================================================
@bot.command()
async def hatchesin(ctx, a: int):
    hatchMin = timedelta(minutes=a)
    raidDuration = timedelta(minutes=45)
    pstDelta = timedelta(hours=7)
    currentTime = datetime.now() - pstDelta
    hatchTime = currentTime + hatchMin
    despawnTime = currentTime + hatchMin + raidDuration 
    await ctx.send("Reported at {:%I:%M%p}".format(currentTime))
    await ctx.send("Hatches in {} minutes.".format(a))
    await ctx.send("Hatches at {:%I:%M%p}".format(hatchTime))
    #await ctx.send("Despawns at: {}:{}".format("{0:0=2d}".format(despawnTime.hour), "{0:0=2d}".format(despawnTime.minute)))
    await ctx.send("Despawns at {:%I:%M%p}".format(despawnTime))

#Despawn from hatch time ===============================================================
@bot.command()
async def hatchesat(ctx, a):
    hatchesAt = datetime.strptime(a, "%I:%M%p")
    raidDuration = timedelta(minutes=45)
    despawnTime = hatchesAt + raidDuration
    await ctx.send("Hatches at {:%I:%M%p}".format(hatchesAt))
    await ctx.send("Despawns at {:%I:%M%p}".format(despawnTime))

#Despawn from time remaining on boss ====================================================
@bot.command()
async def timeleft(ctx, a: int):
    timeRemaining = timedelta(minutes=a)
    pstDelta = timedelta(hours=7)
    currentTime = datetime.now() - pstDelta
    despawnTime = currentTime + timeRemaining 
    await ctx.send("Reported at {:%I:%M%p}".format(currentTime))
    await ctx.send("Despawns in {} minutes".format(a))
    await ctx.send("Despawns at {:%I:%M%p}".format(despawnTime))
 
#TO DO: Add X emoji to bot message.  Delete bot message upon user adding that reaction (2 emojies = delete message).
#http://discordpy.readthedocs.io/en/latest/api.html#discord.on_reaction_add
#@client.event
#async def on_reaction_add(reaction, user):
    #client.delete_message(reaction.message)


#Quest Reporter ===============================================================================

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scope)
credentials = ServiceAccountCredentials(JSON_KEY['client_email'],
                                        JSON_KEY['private_key'].encode(),
                                        SCOPE)
gc = gspread.authorize(credentials)
wksheet = gc.open("QuestReporter").sheet1

@bot.command()
async def sheet(ctx):
    await ctx.send("Sheet: <https://www.goo.gl/8h8jdQ>")

async def report(ctx, stopName, stopLoc, stopReward):
    timeStamp = currentTime = datetime.now() - pstDelta
    formattedTimeStamp = "{:%m/%d %I:%M%p}".format(timeStamp)
    reporterName = discord.Message.author.name
    await ctx.append_row([stopName, stopLoc, stopReward, reporterName, formattedTimeStamp])
    await ctx.send("Thanks for reporting, " reporterName "!  Type -sheet to see today's quests.")
  
  
#TO DO: MemberExporter ========================================================================
    #export list of members with team affliation to csv
    #page 482 in python library - csv module 
@bot.command()
async def exportmembers(ctx):
    await bot.request_offline_members(ctx.message.server) 
    memberNames = [m.display_name for m in ctx.message.server.members]  #obtains members of server where command was entered
    nameColors = [n.display_name.colour for n in ctx.message.server.members]
    with open('memberlist.csv', mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        for v in memberNames:     #iterates through list to create a new row for each name
            writer.writerow([v])  #if by itself without for-loop, would create columns for each name
    await bot.send_file(ctx.message.author, 'temp.csv', filename='memberlist.csv', content="Check your DM for the csv!")
  
@bot.command()
async def testexport(ctx):
    myRow = ['a', 'b', 'c']
    with open('temp.csv', mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        for n in myRow:
            writer.writerow([n])
    await bot.send_file(ctx.message.author, 'temp.csv', filename='myrow.csv', content="Check your DMs.")
                            
  
#bot.run(str(os.environ.get('BOT_TOKEN')))
bot.run(bot_token)

