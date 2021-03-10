from dotenv import load_dotenv
from os import getenv

load_dotenv()

botPrefix = "ch."
TOKEN = getenv("DISCORD_TOKEN")
OWNER_ID = getenv("OWNER_ID")