import discord
from custom.logging import load_database, write_database, check_user
class commands:
    async def show_warnings_table(args:list[str], mentions:list[discord.User],message:discord.Message):
        #load the database
        database = load_database()
        #create a string to load the table into
        content = ""
        for user in database:
            row = database[user]
            if user.isdigit():
                user_name = await message.guild.fetch_member(user)
            else:
                class user_name:
                    display_name = user
            content+= f"{user_name.display_name} | {row['warnings']}\n"
        if len(content) > 2000:
            #split the content
            _content = content.split("\n")[:-1]
            while _content:
                __content = []
                [__content.append(line) if (not sum([len(i) for i in __content])+len(line)+len(__content)+1> 2000) else None for line in _content]
                [_content.pop(_content.index(line)) for line in __content]
                await message.channel.send("\n".join(__content))
        else:
            await message.channel.send(content)
    async def warn(args:list[str], mentions:list[discord.User],message:discord.Message):
        user = mentions[0]
        #check the user
        check_user(user.id)
        #load the database
        database = load_database()
        database[str(user.id)]['warnings']+=1
        write_database(database)
        await message.channel.send(f"{user.display_name} has been warned!")
        pass
    async def unwarn(args:list[str], mentions:list[discord.User], message:discord.Message):
        user = mentions[0]
        #check the user
        check_user(user.id)
        #load the database
        database = load_database()
        database[str(user.id)]['warnings']-=1
        write_database(database)
        await message.channel.send(f"{user.display_name} has been unwarned!")
        pass
    async def help(args:list[str], mentions:list[discord.User], message:discord.Message):
        #laod the database that stores the help texts
        db = load_database("help.json")
        if not len(args) == 1:
            args.append("1")
        if not args[0].isdigit():
            await message.channel.send("please choose a real page number "+str([*db]))
            return
        if not args[0] in db:
            await message.channel.send("please choose a real page number "+str([*db]))
            return
        #assemble the embed
        embedVar = discord.Embed(title=f"Help page {args[0]}", description="The help panel", color=0x19706e)
        for cmd in db[args[0]]:
            embedVar.add_field(name=cmd, value=db[args[0]][cmd], inline=False)
        await message.channel.send(embed=embedVar)