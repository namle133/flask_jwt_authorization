
import psycopg2
from util.salt_hash import *


def create_user_info(conn: psycopg2.extensions.connection):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # drop table
            cur.execute('DROP TABLE IF EXISTS user_info')
            # create table
            create_script = ''' CREATE TABLE IF NOT EXISTS user_info(
                                            username varchar(40) NOT NULL,
                                            email varchar(50) NOT NULL,
                                            password bytea NOT NULL,
                                            verification_code varchar(10) DEFAULT 0,
                                            PRIMARY KEY (username, email))'''
            cur.execute(create_script)
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def add_user_info(conn: psycopg2.extensions.connection, username: str, email: str, password: str):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # insert values into table
            insert_script = 'INSERT INTO user_info (username, email, password) VALUES (%s, %s, %s)'
            value = (username, email, password)
            cur.execute(insert_script, value)
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def check_user_password(conn: psycopg2.extensions.connection, username: str, password: str) -> bool:
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # select values in table
            cur.execute('SELECT * FROM user_info')
            for record in cur.fetchall():
                hashed_pwd = bytes(record["password"])
                if record["username"] == username and verify_password(password, hashed_pwd):
                    return True
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def check_user_email(conn: psycopg2.extensions.connection, email: str) -> bool:
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # select values in table
            cur.execute('SELECT * FROM user_info')
            for record in cur.fetchall():
                if record["email"] == email:
                    return True
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def check_verification_code(conn: psycopg2.extensions.connection, email: str, verified_code: str) -> int:
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # select values in table
            cur.execute('SELECT * FROM user_info')
            for record in cur.fetchall():
                if record["email"] == email:
                    if record["verification_code"] == "0":
                        return 0
                    if record["verification_code"] == verified_code:
                        return 1
            return 2
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def delete_account_user(conn: psycopg2.extensions.connection, username: str):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # deleta values in table
            delete_script = 'DELETE FROM user_info WHERE username = %s'
            delete_record = (username, )
            cur.execute(delete_script, delete_record)
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def update_new_password(conn: psycopg2.extensions.connection, username: str, new_password: str):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # update values in table
            update_script = 'UPDATE user_info SET password = %s WHERE username = %s'
            update_record = (new_password, username)
            cur.execute(update_script, update_record)
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def update_verification_code(conn: psycopg2.extensions.connection, email: str, verified_code: str):
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # update values in table
            update_script = 'UPDATE user_info SET verification_code = %s WHERE email = %s'
            update_record = (verified_code, email)
            cur.execute(update_script, update_record)
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
