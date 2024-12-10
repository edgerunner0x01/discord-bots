import discord
from discord.ext import commands
import logging
import json
from zProbe.Lib.zProbe import Target
from zProbe.Lib import zProbe
zProbe.logger = zProbe.Log("DEBUG").logger
from zProbe.Lib.zProbe import *  # Replace with the actual import of your Target class
zProbe.logger = zProbe.Log("DEBUG").logger

# Set up logging (optional)
logging.basicConfig(level=logging.INFO)

# Load the bot token from config.json
with open('config.json', 'r') as f:
    config = json.load(f)
    bot_token = config.get('token')

# Set up the bot with the appropriate intents
intents = discord.Intents.default()
intents.message_content = True  # Allow the bot to read message content

bot = commands.Bot(command_prefix="!", intents=intents)

# Helper function to format the output cleanly
def format_output(success, data, error_message=None):
    if success:
        return f"**Success:**\n```{data}```"
    else:
        return f"**Error:** {error_message or data}"

# Command to extract meta tags from a URL
@bot.command(name="meta")
async def extract_meta_tags(ctx, url: str):
    try:
        target = Target(url)
        metadata, success = target.Extract_MetaData()
        response = format_output(success, metadata, "Error extracting meta tags.")
        await ctx.send(response)
    except Exception as e:
        logging.error(f"Exception occurred while extracting meta tags: {e}")
        await ctx.send(f"**Error:** Exception occurred: {e}")

# Command to extract HTML source from a URL
@bot.command(name="source")
async def extract_source(ctx, url: str):
    try:
        target = Target(url)
        if target.HTTP_STATUS == 200:
            source = target.source  # Assuming target has the raw source HTML
            response = format_output(True, source)
        else:
            response = format_output(False, f"HTTP Status {target.HTTP_STATUS}", "Error extracting HTML source.")
        await ctx.send(response)
    except Exception as e:
        logging.error(f"Exception occurred while extracting HTML source: {e}")
        await ctx.send(f"**Error:** Exception occurred: {e}")

# Command to extract URLs from a URL
@bot.command(name="urls")
async def extract_urls(ctx, url: str):
    try:
        target = Target(url)
        urls, success = target.Extract_URLS()
        response = format_output(success, urls, "Error extracting URLs.")
        await ctx.send(response)
    except Exception as e:
        logging.error(f"Exception occurred while extracting URLs: {e}")
        await ctx.send(f"**Error:** Exception occurred: {e}")

# Command to extract email addresses from a URL
@bot.command(name="emails")
async def extract_email_addresses(ctx, url: str):
    try:
        target = Target(url)
        emails, success = target.Extract_Emails()
        response = format_output(success, emails, "Error extracting emails.")
        await ctx.send(response)
    except Exception as e:
        logging.error(f"Exception occurred while extracting emails: {e}")
        await ctx.send(f"**Error:** Exception occurred: {e}")

# Command to extract robots.txt from a URL
@bot.command(name="robots")
async def extract_robots_txt(ctx, url: str):
    try:
        target = Target(url)
        content, status_code, success = target.Extract_Robots()
        response = format_output(success, content, "Error extracting robots.txt.")
        await ctx.send(response)
    except Exception as e:
        logging.error(f"Exception occurred while extracting robots.txt: {e}")
        await ctx.send(f"**Error:** Exception occurred: {e}")

# Command to extract URLs from a sitemap.xml file
@bot.command(name="sitemap")
async def extract_urls_from_sitemap(ctx, url: str):
    try:
        target = Target(url)
        urls, status_code, success = target.Extract_Sitemap()
        response = format_output(success, urls, "Error extracting URLs from sitemap.xml.")
        await ctx.send(response)
    except Exception as e:
        logging.error(f"Exception occurred while extracting URLs from sitemap.xml: {e}")
        await ctx.send(f"**Error:** Exception occurred: {e}")

# Command to extract URLs from an XML file
@bot.command(name="xmlurls")
async def extract_urls_from_xml(ctx, url: str):
    try:
        target = Target(url)
        urls, status_code, success = target.Extract_XML_URLS()
        response = format_output(success, urls, "Error extracting URLs from XML content.")
        await ctx.send(response)
    except Exception as e:
        logging.error(f"Exception occurred while extracting URLs from XML: {e}")
        await ctx.send(f"**Error:** Exception occurred: {e}")

# Command to extract WordPress login form parameters
@bot.command(name="wp-login")
async def extract_wp_login_form_params(ctx, url: str):
    try:
        target = Target(url)
        form_params, status_code, success = target.Extract_WPLOGIN()
        response = format_output(success, form_params, "Error extracting WordPress login form parameters.")
        await ctx.send(response)
    except Exception as e:
        logging.error(f"Exception occurred while extracting WP login form parameters: {e}")
        await ctx.send(f"**Error:** Exception occurred: {e}")

# When the bot is ready, print a message
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

# Run the bot with the token loaded from config.json
bot.run(bot_token)
