import os
from dotenv import load_dotenv


load_dotenv()


APPROVED_THRESHOLD = float(os.getenv('APPROVED_THRESHOLD'))
SERVER_HOST = os.getenv('SERVER_HOST')
