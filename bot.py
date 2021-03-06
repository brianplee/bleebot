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

#Quests
# -report 
# -clearoldquests

#Raids
# -find  
# -hatchesin 
# -hatchesat
# -timeleft


#Get token from heroku config'd var 
bot_token = os.environ['BOT_TOKEN']

#client_key = os.environ['CLIENT_KEY']
#client_email = os.environ['CLIENT_EMAIL']
#client_secret = os.environ['CLIENT_SECRET']

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


#===============================================================================
@bot.command() 
async def info():
    #embed = discord.Embed(title="QuestBot", description="I need quest reports to stay alive.", color=0xeee657)
    #embed = embed.add_field(name="Author", value="bleeinyourself")
    #embed.add_field(name="Server Count", value=f"{len(bot.guilds)}")
    #embed = embed.add_field(name="Add me to your server:", value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=469366032176381952&scope=bot)")
    #await bot.say(embed=embed)
    invite_link = 'https://discordapp.com/oauth2/authorize?client_id=469366032176381952&scope=bot'
    await bot.say("Hi, I'm QuestBot.  Add me to your server: {}".format(invite_link))

@bot.command()
async def questbot():
    embed = discord.Embed(title="List of commands:")
    embed.add_field(name="-questbot", value="Gives this message", inline=False)
    embed.add_field(name="-info", value="Gives info about this bot, including an invite link", inline=False)
    embed.add_field(name="-hatchesin", value="-hatchesin minutes \nEx) -hatchesin 45", inline=False)    
    embed.add_field(name="-hatchesat", value="-hatchesat HH:MMpm/am \nEx) -hatchesat 3:30pm", inline=False)    
    embed.add_field(name="-timeleft", value="-timeleft minutes \nEx) -timeleft 56", inline=False)
    embed.add_field(name="-sheet", value="Gives the google sheets link with reported quests", inline=False)
    embed.add_field(name="-report", value='-report <pokestop name>, <pokestop location>, <quest notes> \n\nEx) -report Doyle Park, 61st and hollis, hatch 5 eggs for Chansey \n\nAll 3 parameters are required.  \n\nPlease separate each parameter with a comma. \n\nDo not use commas within a single parameter.', inline=False)
    await bot.say(embed=embed)
  
#http://www.fileformat.info/info/emoji/list.htm
@bot.command()
async def greet():
    await bot.say(":smiley: :wave: Hi.  I am Questbot.")

#=====================================Google Sheets ======================================================

#CAN'T CALL VARS FROM CONFIG VAR SO SCREW IT HERE IT IS.
# look at data types in Heroku.  Why does CLIENT_X509 work but not others?
# look at ServiceAccountCredentials methods for JSON/DICT

client_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCZ3LW+8miTEMY0\n3Bh03uINLulMHJsOEem+a9xPlrQMlh6RsCTcOGjVyOQ298WGRBD4JW9shdqpBk60\noXnyYc7bEZ8FI2K6H/0iYul6uahxv9NIsAAmm7PhTvSZf2yxzOSyZ+AO4y7ToCUw\n66OkQOub9w49lJJzVhuwf0SAgasUGiS6U6ZgvaVYHsaCHEoUOnYNxJ/7npR3ub+e\nJqDPGCvZd8+CgPNYXaMJ5chjzVlxB5/pib5xyYohtdaiZBdA+6buVLn3wVvbR7iL\nqPq1VHX9dR74Fr4Y3z0TKM0xjON7WOOA2X9a+EsXh5OCbNJAdyOAdgzjUNgrmhVD\nCngkBamNAgMBAAECggEAEDQ0V9XDualMloiPcs9+UxEbtM5Wbhbo3QsS+rbOY3zz\n3zgDycWPFOTBVCCoBsnoV5npsC4wpxho9ZED/MjcNioW6z2cyilQSWzNVgVzffdL\n0x3mBirjuNjN3dSTp+4CL9/MswSuC8+T2yEV7NiBd71/HHEnM0pgRChDGJ2PXOBy\nFXCw+2rzYc0g/8+0cssE+LfTtyqQmq2AOkSHymOmUcuayLZNMTxodspdMC/+L369\nU4ATV20NOEyCkLY5mUFABJJ1CbItlXTG3sXcckVowUtuf+Q7Hh2WreyDm56R6ceq\nCPQ7yhJLn6FvL17xs6MUTQIRvgNLmDvMfYPiRefYaQKBgQDT0FW8eWyYxGm4xIt+\nsHQ6nBGEIvar0yhQYfI9auWSx6iZ0gVUa6o7ysNJ6CNyVWgQX3ISuvGx30eCmrKA\n6XPl/yDuwuZa5Io8vGfHIcTNDte/Rb4o2gslqOJK5j8uXfpUlE0h47p3fW2KKoiF\ngn7vBDZrrq5KuzCBWDRW4NF5gwKBgQC59YkP9GABDQyO2v1P7vVYm28kfRsL+zVE\ng+jxkCJAcYGYMMbFJSrrsKz91QIqL9cqkdRbZO6rLml5ckNXmo8M5xlTUtqV3AWA\nbO/teFeKatyVgNcGW/SgqzbMxG9nNhZi/FbHT7MeYSpTfq8SafedJu0ctu7mU24T\ndemlwh+zrwKBgF4DzdpPRv1zyL1DN+tupNhS549v+W8A1ZcAMoZCSU3iIxrLVqRG\n+ZN6hz3ptLoN4JfL1ZUstxTNVy9IPMztUg0XNeXkSlyzrgwRUDrZ6UFfQjHa4fG9\n/k6j7HV0RzzsZ61c+fN94gkhehpmkJw59N9gTktziFcRSRFQNkMNnMzDAoGAJPMS\nvubRxKOxIRmGR8G1YlvQI7HwE9tgZDLJsGXxSFjFZVYbyMRv2NEMLouKmJNU75J2\nXYqamczpDEaV9uwxDGFG+PV3lVtYhIIg0lCdJFXDarllAFB5NQuQIfPOJvXqUNTO\n8V92ucyYumprov8HQmSfrJr0sTNWpetB97uwzOUCgYEA0VYMCCZKEIua/3N3fbD1\nTtKiMfa8rBrewoHlXdwTsjl2lCoTB2r6f3QAD+5suX2NrKuvROEDecp2N7yGeqYC\nOBRR28S9Wwx0VfsJsbTdu/z17uV9TRorddGR6I0YPyfoWhpefnji22Z0Am8UiCR6\nQqVEzkRcrCTIIUczx1mz47Y=\n-----END PRIVATE KEY-----\n"
client_email = "bleebot@gymdatabase-215200.iam.gserviceaccount.com"
CLIENT_SECRET = {
    "type": "service_account",
    "project_id": "gymdatabase-215200",
    "private_key_id": "683bafabe6d2e0fa6f746394f06c4c6c656a655f",
    "private_key": client_key,
    "client_email": client_email,
    "client_id": "117441405217429647940",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ['CLIENT_X509']
   } 


#=====================================Quest Reporter ======================================================
#'-report' => Writes stop, location, quest notes to google sheet
#'-sheet' => Returns link to google sheet 
#'-clearsheet' => clears quests where the timestamp != today's date in the google sheets
#use the _from_parsed_json_keyfile oauth2client method to call hidden client_secrets var with parsed .json contents
# credentials = ServiceAccountCredentials._from_parsed_json_keyfile(client_secret, scope)
@bot.command()
async def sheet():
    await bot.reply("what's good?  Here are today's reported quests: <https://bit.ly/2TNp91e>")
    #goo.gl/5afqk6
    #goo.gl/8h8jdQ
    #https://bit.ly/2TNp91e


@bot.command(pass_context=True)
async def report(ctx, *, stopInfo):
   scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
   credentials = ServiceAccountCredentials._from_parsed_json_keyfile(CLIENT_SECRET, scope)
   gc = gspread.authorize(credentials)
   wksheet = gc.open("QuestReport").get_worksheet(0)
   pstDelta = timedelta(hours=7)  #8 for daylight savings, 7 for normal
   timeStamp = datetime.now() - pstDelta    
   formattedTimeStamp = "{:%m/%d/%Y %I:%M%p}".format(timeStamp)  
   stopName, stopLoc, stopReward = stopInfo.split(",")
   wksheet.append_row([stopName, stopLoc, stopReward, formattedTimeStamp])
   await ctx.bot.add_reaction(ctx.message, emoji="✅")
   
#===================================Clear Quest Sheet =====================================
@bot.command(pass_context=True)
async def clearoldquests(ctx):
   scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
   credentials = ServiceAccountCredentials._from_parsed_json_keyfile(CLIENT_SECRET, scope)
   gc = gspread.authorize(credentials)
   wksheet = gc.open("QuestReport").sheet1
   pstDelta = timedelta(hours=7)
   current_time = datetime.now() - pstDelta
   current_time_date = current_time.date()
   last_row = len(wksheet.get_all_records())
   for r in reversed(range(2, last_row+2)):
       quest_timestamp = wksheet.cell(r, 4).value
       quest_date = datetime.strptime(quest_timestamp, '%m/%d/%Y %I:%M%p').date()
       if quest_timestamp is not None and quest_date != current_time_date:
           wksheet.delete_row(r)
   await ctx.bot.add_reaction(ctx.message, emoji="✅")
   #await bot.say("The quests from yesterday have been cleared.  Today's quests, if there were any, are still in the sheet.")

#=================================== Raid RSVP ===================================================
@bot.command(pass_context=True)
async def find(ctx, *, query):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials._from_parsed_json_keyfile(CLIENT_SECRET, scope)
    gc = gspread.authorize(credentials)
    wksheet = gc.open("QuestReport").get_worksheet(1)
    last_row = len(wksheet.get_all_records())
    list_of_lists = wksheet.get_all_values()  #returns list of lists of gym items (including headers)
    for l in list_of_lists[1:last_row+1]:
        if str(query) in l[0]:
            bot_message = await bot.say(l[4])
            bot_message
            #await bot.add_reaction(bot_message, emoji="⭕")

#===================================Despawn from minutes until hatch =====================================
@bot.command()
async def hatchesin(a: int):
    hatchMin = timedelta(minutes=a)
    raidDuration = timedelta(minutes=45)
    pstDelta = timedelta(hours=7)
    currentTime = datetime.now() - pstDelta
    hatchTime = currentTime + hatchMin
    despawnTime = currentTime + hatchMin + raidDuration 
    await bot.say("Reported at {:%I:%M%p}".format(currentTime))
    await bot.say("Hatches in {} minutes.".format(a))
    await bot.say("Hatches at {:%I:%M%p}".format(hatchTime))
    #await ctx.send("Despawns at: {}:{}".format("{0:0=2d}".format(despawnTime.hour), "{0:0=2d}".format(despawnTime.minute)))
    await bot.say("Despawns at {:%I:%M%p}".format(despawnTime))

#====================================Despawn from hatch time =============================================
@bot.command()
async def hatchesat(a):
    hatchesAt = datetime.strptime(a, "%I:%M%p")
    raidDuration = timedelta(minutes=45)
    despawnTime = hatchesAt + raidDuration
    await bot.say("Hatches at {:%I:%M%p}".format(hatchesAt))
    await bot.say("Despawns at {:%I:%M%p}".format(despawnTime))

#=================================Despawn from time remaining on boss ======================================
@bot.command()
async def timeleft(a: int):
    timeRemaining = timedelta(minutes=a)
    pstDelta = timedelta(hours=7)
    currentTime = datetime.now() - pstDelta
    despawnTime = currentTime + timeRemaining 
    await bot.say("Reported at {:%I:%M%p}".format(currentTime))
    await bot.say("Despawns in {} minutes".format(a))
    await bot.say("Despawns at {:%I:%M%p}".format(despawnTime))

#============================================== Tip =========================================================    
@bot.command()
async def tip(a: float, b: float):
    c = a*b/100
    await bot.say("A {}% tip for a ${} meal or service would be: ${}".format(round(b,2), round(a,2), round(c,2)))
    
#=============================================================================================================
    
#bot.run(str(os.environ.get('BOT_TOKEN')))
bot.run(bot_token)

