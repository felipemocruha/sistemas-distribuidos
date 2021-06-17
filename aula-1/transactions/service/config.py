import os


CASSANDRA_HOSTS = os.getenv('CASSANDRA_HOSTS').split(',')
KAFKA_HOSTS = os.getenv('KAFKA_HOSTS')
