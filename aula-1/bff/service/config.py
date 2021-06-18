import os
from dotenv import load_dotenv


load_dotenv()


REDIS_HOST = os.getenv('REDIS_HOST')
KAFKA_HOSTS = os.getenv('KAFKA_HOSTS')
FAILURE_RATE = float(os.getenv('FAILURE_RATE')) or 0.0
