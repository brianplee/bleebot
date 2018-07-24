 
#to get updated discord.py, CMD: pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip
import datetime
from datetime import time
from datetime import datetime
from datetime import timedelta
import asyncio 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os 

#Getting api key from heroku
bot_token = os.environ['BOT_TOKEN']

bot = commands.Bot(command_prefix='-')
                   
#the command_prefix is what must be typed to invoke a command

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
#def function_name(ctx, arg1, arg2...)
#enter "prefix+function argument" ('-hatchesin 120')

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
    embed.add_field(name="-guide", value="Gives this message")
    embed.add_field(name="-info", value="Gives info about this bot")
    embed.add_field(name="-tip price percent", value="Calculates your tip.  Ex) -tip 20 15")
    embed.add_field(name="-hatchesin minutes HH:MMam/pm", value="Gives the hatch time and despawn time given minutes left until hatch.  Ex) -hatchesin 45 9:30am")
    embed.add_field(name="-hatchTime HH:MMam/pm", value="Gives the despawn time given minutes left until hatch")
    embed.add_field(name="-timeleft minutes HH:MMam/pm", value="Gives the despawn time given minutes left until despawn.  Ex) -timeleft 45 9:30am")
    await ctx.send(embed=embed)
    
@bot.command()
async def add(ctx, a: float, b: float):
    await ctx.send(a+b)

@bot.command()
async def multiply(ctx, a: float, b: float):
    await ctx.send(a*b)

@bot.command()
async def tip(ctx, a: float, b: float):
    await ctx.send("A {}% tip for a ${} meal or service would be: $".format(b, a),.send(a*b/100))

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hi.  I am Bleebot.")

#TO DO: MemberExporter ========================================================================
    #export list of members with team affliation to csv
    
#TO DO: GymDataBase ===========================================================================
    #store gym name, googlemaps link, and description in free database (google sheets)
    #call gym info from google sheets


#Despawn from minutes until hatch ======================================================
@bot.command()
async def hatchesin(ctx, a: int, b):
    timeReported = datetime.strptime(b,"%H:%M%p")
    hatchMin = timedelta(minutes=a)
    currentTime = datetime.now()
    raidDuration = timedelta(minutes=45)
    await ctx.send("Hatches in", a, "minutes.")
    await ctx.send("Hatch time:", timeReported + hatchMin)
    await ctx.send("Despawn time:", timeReported + hatchMin + raidDuration)

#Despawn from hatch time ===============================================================
@bot.command()
async def hatchtime(ctx, a):
    hatchesAt = datetime.strptime(a, "%H:%M%p")
    raidDuration = timedelta(minutes=45)
    await ctx.send("Despawns at:", hatchesAt + raidDuration)

#Despawn from time remaining on boss ====================================================
@bot.command()
async def timeleft(ctx, a: int, b):
    timeRemaining = timedelta(minutes=a)
    timeReported = datetime.strptime(b, "%H:%M%p")
    await ctx.send("Minutes before despawn:", a, "minutes.")
    await ctx.send("Despawn time:", timeReported + timeRemaining)

#if __name__ == '__main__':
    #import config
    #client.run(config.token)
    #bot.run(Token)
    
#bot.run(str(os.environ.get('BOT_TOKEN')))
bot.run(bot_token)

