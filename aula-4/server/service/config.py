import os
from dotenv import load_dotenv


load_dotenv()


KAFKA_HOSTS = os.getenv("KAFKA_HOSTS")
KAFKA_USER = os.getenv("KAFKA_USER")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")

SECRET_KEY = os.getenv("SECRET_KEY")
DB_NAME = os.getenv("DB_NAME")
