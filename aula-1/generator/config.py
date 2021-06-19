import os
from dotenv import load_dotenv


load_dotenv()


BFF_HOST = os.getenv('BFF_HOST')
REQUEST_INTERVAL = int(os.getenv('REQUEST_INTERVAL'))
