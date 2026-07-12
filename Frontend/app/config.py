# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", ""),
    BASE_URL = os.getenv('BASE_URL','')
