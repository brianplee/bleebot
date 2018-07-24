 
#Locally: CMD ->pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip
#Declare dependents on Heroku: git+https://github.com/Rapptz/discord.py@rewrite
import datetime
from datetime import time
from datetime import datetime
from datetime import timedelta
import asyncio 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os 

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
async def savvyt(ctx):
    await ctx.send("Go back to bed.")

@bot.command()
async def guide(ctx):
    embed = discord.Embed(title="List of commands:")
    embed.add_field(name="-guide", value="Gives this message", inline=False)
    embed.add_field(name="-info", value="Gives info about this bot, including an invite link", inline=False)
    embed.add_field(name="-tip price percent", value="Calculates your tip.  Ex) -tip 20 15", inline=False)
    embed.add_field(name="-hatchesin (minutes)", value="Gives the hatch time and despawn time given minutes left until hatch.  Ex) -hatchesin 45", inline=False)
    embed.add_field(name="-hatchesat (HH:MMam/pm)", value="Gives the despawn time given the hatch time.  Ex) -hatchesat 09:30am", inline=False)
    embed.add_field(name="-timeleft (minutes)", value="Gives the despawn time given minutes left until despawn.  Ex) -timeleft 45", inline=False)
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
    await ctx.send("Reported time: {}:{}".format("{0:0=2d}".format(currentTime.hour), "{0:0=2d}".format(currentTime.minute)))
    await ctx.send("Hatches in {} minutes.".format(a))
    await ctx.send("Hatch time: {}:{}".format("{0:0=2d}".format(hatchTime.hour), "{0:0=2d}".format(hatchTime.minute)))
    await ctx.send("Despawn time: {}:{}".format("{0:0=2d}".format(despawnTime.hour), "{0:0=2d}".format(despawnTime.minute)))

#Despawn from hatch time ===============================================================
@bot.command()
async def hatchesat(ctx, a):
    hatchesAt = datetime.strptime(a, "%H:%M%p")
    raidDuration = timedelta(minutes=45)
    despawnTime = hatchesAt + raidDuration
    await ctx.send("Hatches at: {}:{}".format("{0:0=2d}".format(hatchesAt.hour), "{0:0=2d}".format(hatchesAt.minute)))
    await ctx.send("Despawns at: {}:{}".format("{0:0=2d}".format(despawnTime.hour), "{0:0=2d}".format(despawnTime.minute)))

#Despawn from time remaining on boss ====================================================
@bot.command()
async def timeleft(ctx, a: int):
    timeRemaining = timedelta(minutes=a)
    pstDelta = timedelta(hours=7)
    currentTime = datetime.now() - pstDelta
    despawnTime = currentTime + timeRemaining 
    await ctx.send("Reported at {}:{}".format("{0:0=2d}".format(currentTime.hour), "{0:0=2d}".format(currentTime.minute)))
    await ctx.send("Despawns in {} minutes".format(a))
    await ctx.send("Despawns at {}:{}".format("{0:0=2d}".format(despawnTime.hour), "{0:0=2d}".format(despawnTime.minute)))
 
#TO DO: Add X emoji to bot message.  Delete bot message upon user adding that reaction (2 emojies = delete message).
#http://discordpy.readthedocs.io/en/latest/api.html#discord.on_reaction_add
#@client.event
#async def on_reaction_add(:smiley:, user):
    #client.delete_message(:smiley:.message)

#TO DO: MemberExporter ========================================================================
    #export list of members with team affliation to csv
    
#TO DO: GymDataBase ===========================================================================
    #store gym name, googlemaps link, and description in free database (google sheets)
    #call gym info from google sheets
  
#bot.run(str(os.environ.get('BOT_TOKEN')))
bot.run(bot_token)

