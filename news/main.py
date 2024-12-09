import discord
from discord.ext import commands, tasks
import aiohttp
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO)

# Read the API key and bot token from a config file (you can replace this with environment variables or direct assignment)
def load_config():
    try:
        with open("config.json") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Config file not found! Please create a 'config.json' file with the API key and bot token.")
        raise
    except json.JSONDecodeError:
        logging.error("Error decoding config.json! Ensure it contains valid JSON.")
        raise

# Load configuration
config = load_config()
api_key = config.get("news_api_key")
bot_token = config.get("bot_token")
channel_id = int(config.get("channel_id"))

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Fetch the news asynchronously using aiohttp
async def fetch_news_data():
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            async with session.get(url) as response:
                response.raise_for_status()  # Raises an error for bad HTTP status
                return await response.json()
    except aiohttp.ClientError as e:
        logging.error(f"Error fetching news data: {e}")
        return None

# Task loop to send news every 10 minutes
@tasks.loop(minutes=1)
async def fetch_news():
    news_data = await fetch_news_data()
    if news_data and news_data["status"] == "ok":
        articles = news_data["articles"]
        channel = bot.get_channel(channel_id)
        if channel:
            for article in articles[:5]:  # Send the top 5 articles
                title = article.get("title", "No title available")
                description = article.get("description", "No description available")
                url = article.get("url", "#")
                await channel.send(f"**{title}**\n{description}\nRead more: {url}\n")
        else:
            logging.error(f"Channel with ID {channel_id} not found.")
    else:
        logging.error("Failed to retrieve news or no articles available.")

# Event triggered when bot is ready
@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')
    fetch_news.start()  # Start the task loop

# Gracefully handle bot shutdown
@bot.event
async def on_shutdown():
    logging.info("Shutting down the bot...")

# Run the bot
try:
    bot.run(bot_token)
except discord.LoginFailure:
    logging.error("Invalid bot token! Please check your bot's token in the config.")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
