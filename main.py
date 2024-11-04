from config import *
import discord
from commands import *
from custom import logging
import os

#move to config after stream
PREFIX = "!"
# move the working dir to the script's dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))


app = discord.Client(intents=discord.Intents.all())

@app.event
async def on_ready():
    print(f"{app.user.display_name} is ready!")

@app.event
async def on_message(message:discord.Message):
    #log the message
    logging.write_log(message)
    if message.author == app.user:
        return
    #check for the prefix
    if message.content.startswith(PREFIX):
        #process message for valid commands
        msg = message.content
        msg = msg[1:] #chop off the prefix
        msg = msg.split(" ")
        msg.append("")
        command, args = msg[0],msg[1:] #divide out the command and it's args
        mentions = message.mentions
        if command in commands.__dict__:
            await commands.__dict__[command](args, mentions, message)

app.run(token)