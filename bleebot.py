 
#to get updated discord.py, CMD: pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip
import datetime
from datetime import time
from datetime import datetime
from datetime import timedelta

import discord
from discord.ext import commands

print(discord.__version__)

bot = commands.Bot(command_prefix='-', description='A bot that does a host of shit.')
                   
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
    embed = discord.Embed(title="BleeBot", Description="Because math is hard.", color=0xeee657)
    embed.add_field(name="Author", value="bleeinyourself")
    embed.add_field(name="Server Count", value=f"{len(bot.guilds)}")
    embed.add_field(name="Add me to your server:", value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=469366032176381952&scope=bot)")
    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed.add_field(name="-help", value="Gives this message", inline=false)
    embed.add_field(name="-info", value="Gives info about this bot", inline=false)
    embed.add_field(name="-tip price percent", value="Calculates your tip.  Ex) -tip 20 15", inline=false)
    embed.add_field(name="-hatchesin minutes HH:MMam/pm", value="Gives the hatch time and despawn time given minutes left until hatch.  Ex) -hatchesin 45 9:30am", inline=false)
    embed.add_field(name="-hatchTime HH:MMam/pm", value="Gives the despawn time given minutes left until hatch", inline=false)
    embed.add_field(name="-timeleft minutes HH:MMam/pm", value="Gives the despawn time given minutes left until despawn.  Ex) -timeleft 45 9:30am", inline=false)

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send("The sum is:", a+b)

@bot.command()
async def multiply(ctx, a: int, b:int):
    await ctx.send("The product is:", a*b)

@bot.command()
async def tip(ctx, a: int, b:int):
    await ctx.send("A", b,"% tip for a $", a, "meal would be: $",a*b/100)

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
async def hatchtime(ctx, a):
    hatchesAt = datetime.strptime(a, "%H:%M%p")
    raidDuration = timedelta(minutes=45)
    await ctx.send("Despawns at:", hatchesAt + raidDuration)

#Despawn from time remaining on boss ====================================================
async def timeleft(ctx, a: int, b):
    timeRemaining = timedelta(minutes=a)
    timeReported = datetime.strptime(b, "%H:%M%p")
    await ctx.send("Minutes before despawn:", a, "minutes.")
    await ctx.send("Despawn time:", timeReported + timeRemaining)

if __name__ == '__main__':
    import config
    client.run(config.token)







=======
 
#to get updated discord.py, CMD: pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip
import datetime
from datetime import time
from datetime import datetime
from datetime import timedelta

import discord
from discord.ext import commands

print(discord.__version__)

bot = commands.Bot(command_prefix='-', description='A bot that does a host of shit.')
                   
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
    embed = discord.Embed(title="BleeBot", Description="Because math is hard.", color=0xeee657)
    embed.add_field(name="Author", value="bleeinyourself")
    embed.add_field(name="Server Count", value=f"{len(bot.guilds)}")
    embed.add_field(name="Add me to your server:", value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=469366032176381952&scope=bot)")
    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed.add_field(name="-help", value="Gives this message", inline=false)
    embed.add_field(name="-info", value="Gives info about this bot", inline=false)
    embed.add_field(name="-tip price percent", value="Calculates your tip.  Ex) -tip 20 15", inline=false)
    embed.add_field(name="-hatchesin minutes HH:MMam/pm", value="Gives the hatch time and despawn time given minutes left until hatch.  Ex) -hatchesin 45 9:30am", inline=false)
    embed.add_field(name="-hatchTime HH:MMam/pm", value="Gives the despawn time given minutes left until hatch", inline=false)
    embed.add_field(name="-timeleft minutes HH:MMam/pm", value="Gives the despawn time given minutes left until despawn.  Ex) -timeleft 45 9:30am", inline=false)

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send("The sum is:", a+b)

@bot.command()
async def multiply(ctx, a: int, b:int):
    await ctx.send("The product is:", a*b)

@bot.command()
async def tip(ctx, a: int, b:int):
    await ctx.send("A", b,"% tip for a $", a, "meal would be: $",a*b/100)

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
async def hatchtime(ctx, a):
    hatchesAt = datetime.strptime(a, "%H:%M%p")
    raidDuration = timedelta(minutes=45)
    await ctx.send("Despawns at:", hatchesAt + raidDuration)

#Despawn from time remaining on boss ====================================================
async def timeleft(ctx, a: int, b):
    timeRemaining = timedelta(minutes=a)
    timeReported = datetime.strptime(b, "%H:%M%p")
    await ctx.send("Minutes before despawn:", a, "minutes.")
    await ctx.send("Despawn time:", timeReported + timeRemaining)

#if __name__ == '__main__':
    #import config
    #client.run(config.token)
  
bot.run('NDY5MzY2MDMyMTc2MzgxOTUy.DjGrNw.XAeqkrsxS8L3xZJJR9-GEmWGh4s')







>>>>>>> f0e38b2e0868d5b0002361a6a8138ae0149953f3
