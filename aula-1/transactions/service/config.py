import os
from dotenv import load_dotenv


load_dotenv()


CASSANDRA_HOSTS = os.getenv('CASSANDRA_HOSTS').split(',')
KAFKA_HOSTS = os.getenv('KAFKA_HOSTS')
ANTIFRAUD_HOST = os.getenv('ANTIFRAUD_HOST')
BFF_HOST = os.getenv('BFF_HOST')
