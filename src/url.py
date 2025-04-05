import os

from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")


def create_url(postfix):
    return f"{API_BASE_URL}{postfix}"
