import discord
import subprocess
import asyncio
import shlex
import json
from discord.ext import commands

# Load the configuration from config.json
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

# Read bot token from config.json
config = load_config()
BOT_TOKEN = config['bot_token']

# Define bot command prefix and description
intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Run system commands (safely executing shell commands)
def run_command(command):
    try:
        # Safely run shell commands
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            return f"Error: {stderr.decode()}"
        return stdout.decode()
    except Exception as e:
        return f"An error occurred while running the command: {str(e)}"

# Define the 'recon' command
@bot.command(name="recon")
async def recon(ctx, *, domain: str):  # Added `*` to capture everything after the command as `domain`
    try:
        # Send a message indicating the scan has started
        await ctx.send(f"Starting recon scan for {domain}... This may take a few moments.")
        
        # Run various tools
        nmap_result = run_command(f"nmap -F {domain}")
        dig_result = run_command(f"dig {domain}")
        #whois_result = run_command(f"whois {domain}")
        nslookup_result = run_command(f"nslookup {domain}")
        
        # Format the results into a report
        report = f"Recon Report for {domain}\n"
        #report += "===========================\n"
        report += f"**Nmap Scan Results**:\n```\n{nmap_result}\n```\n"
        report += f"**Dig Results**:\n```\n{dig_result}\n```\n"
        #report += f"**Whois Info**:\n```\n{whois_result}\n```\n"
        report += f"**Nslookup Results**:\n```\n{nslookup_result}\n```\n"

        # Send the formatted report to Discord
        await ctx.send(report)

    except Exception as e:
        await ctx.send(f"An error occurred while processing the recon scan: {str(e)}")

# Event handler when the bot is ready (successful login)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(f'Bot is ready and listening for commands!')

    # Check if the commands are loaded
    for command in bot.commands:
        print(f"Loaded command: {command.name}")

# Run the bot with the token from config.json
bot.run(BOT_TOKEN)
