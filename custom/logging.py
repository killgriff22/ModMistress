#Never Parse Logs.

#channels/{channelid}/{date}.txt
#--
#{display name} : {user name} : {user id} : {timestamp}
#{message}
#--
#channels/{channelid}/extra-{date}.txt
#--
#[{files}] : {etc.}
#--

import time,datetime
import os, discord, json
from pathlib import Path
def write_log(message:discord.Message):
    #write timestamp
    timestamp = datetime.datetime.now()
    #extract the date
    date = timestamp.strftime("%d%m%Y")
    #get the channel from the message
    channelid = message.channel.id
    #perform the checks for if the file exists
    create_log(channelid,date)
    display_name = message.author.display_name
    user_name = message.author.global_name
    user_id = message.author.id
    #check if the user is in the database
    check_user(user_id)
    #open the file
    with open(f"channels/{channelid}/{date}.txt","a") as f:
        f.write(f"""--
{display_name} : {user_name} : {user_id} : {timestamp.strftime('%H%M%S')} : {message.id}
{message.content}
--
""")
        f.close()
    if message.attachments:
        with open(f"channels/{channelid}/extra-{date}.txt","a") as f:
            f.write(f"""--
{[attachment.url for attachment in message.attachments]} : {message.id}
--
""") 
            f.close()
    pass

def create_log(channelid,date):
    if not os.path.exists(f"channels/{channelid}"):
        os.mkdir(f"channels/{channelid}")
    if not os.path.exists(f"channels/{channelid}/{date}.txt"):
        Path(f"channels/{channelid}/{date}.txt").touch()
    if not os.path.exists(f"channels/{channelid}/extra-{date}.txt"):
        Path(f"channels/{channelid}/extra-{date}.txt").touch()
    pass

def load_database():
    database_file = open("UserDatabase.json","r")
    database = json.loads(database_file.read())
    database_file.close()
    return database

def write_database(database):
    database_file = open("UserDatabase.json","w")
    database_file.write(json.dumps(database))
    database_file.close()
def check_user(userid):
    #read database
    database= load_database()
    #check for userid in database
    if not str(userid) in database:
        database[userid]={'warnings':0}
    #write database changes
    write_database(database)
    del database
    #free memory of database