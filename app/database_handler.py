import sys
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
def login_user(username,password):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    login_command ="""SELECT * FROM users
                    WHERE username = %s;
                    """
    cursor.execute(login_command,(username,))
    row = cursor.fetchone()
    db_password = row[1]
    if row == None or not check_password_hash(db_password, password):
        return False
    return True

def signup_user(email,username,password):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    #check if email already exists
    email_check = """SELECT * FROM users
                     WHERE email = %s;
                """
    #check if username exists
    username_check = """SELECT * FROM users
                        WHERE username = %s;
                    """
    cursor.execute(email_check)
    returnemail = cursor.fetchone()
    cursor.execute(username_check)
    returnusername = cursor.fetchone()
    #None = none found in query
    if returnemail == None and returnusername == None:
        insert_user = """INSERT INTO users(id,email,username,password)
                        VALUES (%s,%s,%s,%s);
                    """
        hashed_pass=generate_password_hash(password, method='sha256')
        cursor.execute(insert_user,(1,email,username,hashed_pass))
        return True #signup good
    return False #signup failed

def bookmark_channel(id,channel):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    #check if bookmark already exists
    check_command = """ SELECT * FROM test_bm
                        WHERE id = %s AND channel = %s;
                    """
    cursor.execute(check_command,(id,channel))
    row = cursor.fetchone()
    if row != None:
        sys.stderr.write("aborted")
        return False #bookmark already exists, abort
    #otherwise, insert into the bookmarks table
    bookmark_command = """ INSERT INTO test_bm(id, channel)
                           VALUES (%s,%s);
                        """
    cursor.execute(bookmark_command,(id,channel))
    cursor.execute("SELECT * FROM test_bm")#Testing Code
    test = str(cursor.fetchall()) #testing
    sys.stderr.write(test)#testing
    conn.commit()
    conn.close()
    return True #returns true for successful bookmark