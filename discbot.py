#bot.py
import sys
import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from pathlib import Path
import traceback
import imp
import copy
import logging
from logging.handlers import TimedRotatingFileHandler

sys.path.append("lib/")
from database import DataBase
from users import UserManager
from commander import CommandArgs
from plugins import PluginManager
def bindfunction(name, comm):
    async def myComm(ctx):
        args = CommandArgs
        args.text= " ".join(ctx.message.content.split(" ")[1:])
        response = comm.command(args)
        await ctx.send(response.getText())
    myComm.__name__ = name
    return myComm

# 1
from discord.ext import commands
log = logging.getLogger("Rotating Log")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
passwd = os.getenv('passwd')
dbname = os.getenv('dbname')
username = os.getenv('username')
prefix = os.getenv('prefix')
dbconn = DataBase(dbname, username, passwd)
pg = PluginManager(log, dbconn, prefix)
commander = pg.get_plugins()
# 2
bot = commands.Bot(command_prefix='!')
for (kw,comm) in commander.items():

    botcomms = bindfunction(kw, comm)
    myhelp = getattr(comm, "myhelp", "No help provided")
    bot.add_command(commands.Command(botcomms, name=kw, help=myhelp))


    

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)

