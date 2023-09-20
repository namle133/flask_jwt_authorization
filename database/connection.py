import redis
import psycopg2
import psycopg2.extras
from database.config_db.config_postgresql import config_postgres
from database.config_db.config_redis import config_redis
from service.user_service import *

PATH_DATABASE_INFO = "database.ini"

Pg = None
Rd = None

def InitPosgres():
    """ Connect to the PostgreSQL database server """
    conn = None   
    params = config_postgres()
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')

    conn = psycopg2.connect(**params)
    global Pg
    Pg = conn

def InitRedis():
    """ Connect to the Redis database server """  
    params = config_redis()
    # connect to the PostgreSQL server
    print('Connecting to the Redis database...')

    user_connection = redis.Redis(**params)
    global Rd
    Rd = user_connection

def InitDB():
    InitRedis()
    InitPosgres()
    create_user_info(Pg)