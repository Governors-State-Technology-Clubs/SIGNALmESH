import discord
import logging
import os
import argparse
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv
from logHandlers import logger_setup
import random


# ========================================= Housekeeping

parser = argparse.ArgumentParser(description="Set Variables for Bot Script")
parser.add_argument('--app', type=str)
parser.add_argument('--version', type=str)
parser.add_argument('--env', type=str)
parser.add_argument('--port', type=str)
args = parser.parse_args()

# You can change the name of the application in the logs by changing the string for logger_setup
std_handlers = logger_setup(args)

logger = logging.getLogger(__name__)
for handler in std_handlers:
    logger.addHandler(handler)

root_dir = Path.cwd()
logger.info(f"Root directory set to {root_dir}")

if args.env is None:
    loaded = load_dotenv(verbose=True)
    if not loaded:
        logger.info("No Environment file provided or discovered.")
        my_env = root_dir / input(f"Enter the .env file name. \nNOTE: The file has to be in the root directory:\n").strip()
        loaded = load_dotenv(dotenv_path=my_env)
        logger.info("Second attempt to set .env")
    if not loaded:
        logger.error("No .env file was located")
        raise EnvironmentError(f"No .env:{my_env} was located")
    logger.info(f"Environment file set")
    
else:
    my_env = root_dir / args.env
    load_dotenv(dotenv_path=my_env)
    logger.info(f"Environment file set to {my_env}")

bot_token = os.getenv("DISCORD_TOKEN")

if bot_token is None:
    raise Exception("DISCORD_TOKEN Not Set")

server_id = os.getenv("GENERAL_CHANNEL_ID")

if server_id is None:
    raise Exception("SERVER_CHANNEL_ID Not Set")

# Discord intents
logger.info("Setting Default Intents")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="==", intents=intents)
logger.info("Housekeeping Complete")

# ========================================= Data
word_list = ['wet','clean', 'python', 'code', 'java', 'brew', 'c++']
swap_list = ['moist','cweem','Black Mamba','chungus', 'brew', 'brew-thingy', 'completely untenable']

magic_8_ball_responses = [
    "Obviously. 🙄",
    "Do I look like I care? Sure, why not.",
    "Mmm… try again when you're serious. 💅",
    "Absolutely not. But hey, dream big. 🌈",
    "LMAO, you wish. 😂",
    "The audacity… but yeah, maybe.",
    "Signs point to... girl, no.",
    "Oh honey, not with that attitude. 😬",
    "Yes, but only if pigs start flying. 🐷✈️",
    "Hmm... let me get back to you never.",
    "Ask your mom. Oh wait, she already knows. 😏",
    "Try manifesting harder. ✨",
    "You’ve got a better chance winning the lottery.",
    "Don't quit your daydream. 😌",
    "Nope. Not today, Satan.",
    "My crystal ball just rolled its eyes. 🙄🔮",
    "You didn’t even say ‘please’. Rude.",
    "I'm gonna pretend I didn't hear that statement."
]

old_balls_nathan = [
    "Nathan? somebody call Nathan for this crap",
    "Dang, do we really gotta hit up Nate for this?",
    "Do you have your Part107 License? If not we should see if Nate knows"
]

old_balls_thomas = [
    "This sounds like a Thomas problem",
    "This sounds like an actual coding statement, try Thomas",
    "Is Thomas still here, he might be the only one who can help"
]

old_balls_brett = [
    "Sound like you need Brett",
    "Its a bird, its a plane, nope, its a Brett statement",
    "Sounds like a club statement, only one that will know is Brett"
]

old_balls_generic = [
    "Back in my day, we just googled it and hoped for the best.",
    "That’s a great statement. Ask again after you use ChatGPT.",
    "Let me put on my glasses and pretend I know what I’m doing."
]

# ========================================= Events
@bot.event
async def on_ready():
    for server in bot.guilds:
        logger.info(f"Logged in as: {bot.user.name} on Server:{server.name} ID:{server.id}")
    logger.info(f"{bot.user.name} Ready")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Word replacement feature
    for word, swap in zip(word_list, swap_list):
        if word in message.content.lower():
            msg = message.content
            msg = msg.replace(word, swap)
            await message.delete()
            await message.channel.send(f"{message.author.mention}: {msg}")
            await message.channel.send(f"{message.author.mention} Hahahahaha")
    await bot.process_commands(message)

# === Old Balls Question (OBQ) Feature ===
@bot.command(aliases=[
    'obq',
    'Obq',
    'OBQ',
    'obq feature',
    'Obq Feature',
    'OBQ Feature',
    'OBQ FEATURE'])
async def obq_feature(ctx: commands.Context):
    response = None
    statement = ctx.message.content.lower()
    obt = ["c++", "python", "java", "javascript", "html"]
    obb = ["jaguar connections", "club", "event"]
    
    if "drone" in statement:
        response = random.choice(old_balls_nathan)
        await ctx.send(response)

    for term in obt:
        if term in statement and response is None:
            response = random.choice(old_balls_thomas)
            await ctx.send(response)
    for term in obb:
        if term in statement and response is None: 
            response = random.choice(old_balls_brett)
            await ctx.send(response)

    if response is None:
        response = random.choice(old_balls_generic)
        logger.info("Old Balls Question Run")
        await ctx.send(response)

@bot.command(aliases=[
    'm8b',
    'M8b',
    'M8B',
    'm8b feature',
    'M8b Feature',
    'M8B Feature',
    'M8B FEATURE'])
async def m8b_feature(ctx: commands.Context):
    response = None
    statement = ctx.message.content.lower()

    response = random.choice(magic_8_ball_responses)
    await ctx.send(f"🎱 {response}")
    
# ========================================= Run the Bot
bot.run(bot_token, log_level=logging.DEBUG) 