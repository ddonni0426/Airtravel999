import os
from dotenv import load_dotenv

load_dotenv()

config = {"DB_URL": os.getenv("DB_URL"), "SECRET_KEY": os.getenv("SECRET_KEY")}
