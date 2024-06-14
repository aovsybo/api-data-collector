import os

from dotenv import load_dotenv

load_dotenv(".env")

API_KEY = os.getenv("API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
