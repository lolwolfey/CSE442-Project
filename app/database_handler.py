import sys
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
class User:
    user_id = None
    email = None
    username = None
    hashedPassword = None
    authenticated = False

   # A user object can be made in 2 ways, username and password or user id. the other values should be none.
    def __init__(self, user_id, username, password):
        if user_id == None:
            user = get_user_by_username(username)
            if user:
                if check_password_hash(user[3], password):
                    self.email = user[1]
                    self.username = user[2]
                    self.hashedPassword = user[3]
                    self.user_id = user[0]
                    self.authenticated = True

        # Exccpets a unicode ID, must return None id an invalid Id is provided.
        elif username == None and password == None:
            try:
                user_id = int(user_id)
            except ValueError:
                return None
            user = get_user_by_id(user_id)
            if not user:
                return None
            self.email = user[1]
            self.username = user[2]
            self.hashedPassword = user[3]
            self.user_id = user[0]
            self.authenticated = True

        else:
            return None

    def login(self, username, password):
        if user_login(username, password):
            self.authenticated = True
        return self.authenticated

    def is_authenticated(self):
        return self.authenticated

    # This is a required method for Flask_login functionality.
    # for now it always returns true, but if we add functionality to ban/suspend users would change this.
    def is_active(self):
        return True
    
    def get_username(self):
        return self.username
    
    # similar to is_active, required for Flask_login
    def is_anonymous(self):
        return False

    # returns unicode user_id
    def get_id(self):
        return str(self.user_id).encode()

def init():
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()

    # Comment/uncomment this to save/delete users table between test deploys
    delete_bookmarks_table = "DROP TABLE bookmarks"
    delete_user_table = "DROP TABLE users;"
    delete_relation = "DROP TABLE idtoname;"
    delete_private_table = "DROP TABLE private;"
    cursor.execute(delete_bookmarks_table)
    cursor.execute(delete_user_table)
    cursor.execute(delete_relation)
    cursor.execute(delete_private_table)

    create_private_relation = """ CREATE TABLE IF NOT EXISTS private(
                                username VARCHAR(100) NOT NULL,
                                privmode INTEGER,
                                PRIMARY KEY (username)
                            );  
                                """

    create_idtoname_relation = """CREATE TABLE IF NOT EXISTS idtoname(
                                channel_id VARCHAR(100),
                                channel_name VARCHAR(100),
                                PRIMARY KEY (channel_id),
                                UNIQUE (channel_name)
                                );
                                """

    create_user_table = """CREATE TABLE IF NOT EXISTS users( 
                        id SERIAL,
                        email TEXT NOT NULL,
                        username VARCHAR(100) NOT NULL,
                        password VARCHAR(100) NOT NULL,
                        PRIMARY KEY (id),
                        UNIQUE (id, email, username)
                        );
                        """
    #serial auto increments ID
    #users(id = PRIMARY KEY, email = UNIQUE, username = UNIQUE, password)
    create_bookmarks_table = """ CREATE TABLE IF NOT EXISTS bookmarks(
                            id INTEGER ,
                            channel TEXT,
                            channel_id TEXT,
                            CONSTRAINT fk_users
                                FOREIGN KEY (id)
                                    REFERENCES users(id)
                                    ON DELETE CASCADE
                            );
                            """
    create_test_table = """ CREATE TABLE IF NOT EXISTS test_bm(
                            id INTEGER ,
                            channel TEXT
                            );
                            """ #delete after
    #bookmarks(id,channel) id->user wants to bookmark a channel.
    #Foreign Key constraint makes deleting channels easier. For example
    #If you delete a user with ID=100, all rows where ID = 100 will be deleted as well.
    cursor.execute(create_test_table) #delete later
    cursor.execute(create_user_table)
    cursor.execute(create_bookmarks_table)
    cursor.execute(create_idtoname_relation)
    cursor.execute(create_private_relation)
    conn.commit()
    conn.close()

def user_login(username,password):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    #look for same username in table
    login_command ="""SELECT * FROM users
                    WHERE username = %s;
                    """
    cursor.execute(login_command,(username,))
    row = cursor.fetchone()
    #then check if password is correct
    if row == None:
        return False
    db_password = row[3]
    if not check_password_hash(db_password, password):
        return False
    conn.commit()
    conn.close()
    return True

def Check_email(email):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    #check if email already exists
    email_check = """SELECT * FROM users
                     WHERE email = %s;
                """
    cursor.execute(email_check,(email,))
    returnemail = cursor.fetchone()

    if returnemail != None:
        return True
    conn.commit()
    conn.close()
    return False

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
    cursor.execute(email_check,(email,))
    returnemail = cursor.fetchone()
    cursor.execute(username_check,(username,))
    returnusername = cursor.fetchone()
    #None = none found in query
    if returnemail == None and returnusername == None:
        insert_user = """INSERT INTO users(email,username,password)
                        VALUES (%s,%s,%s);
                    """
        insert_private = """INSERT into private(username, privmode)
                            VALUES (%s,%s);
                        """
        hashed_pass=generate_password_hash(password, method='sha256')
        cursor.execute(insert_user,(email,username,hashed_pass))
        cursor.execute(insert_private,(username,0))
        conn.commit()
        conn.close()
        return True #signup good
    conn.commit()
    conn.close()
    return False #signup failed

def get_user_by_username(username):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    username_check = """SELECT * FROM users
                    WHERE username = %s;
                """
    cursor.execute(username_check,(username,))
    row = cursor.fetchone()
    if row == None:
        return False
    conn.commit()
    conn.close()
    return row

def get_user_by_id(id):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    id_check = """SELECT * FROM users
                    WHERE id = %s;
                """
    cursor.execute(id_check,(id,))
    row = cursor.fetchone()
    if row == None:
        return False
    conn.commit()
    conn.close()
    return row

def has_bookmark(id,channel,channel_id):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    #check if bookmark already exists
    check_command = """ SELECT * FROM bookmarks
                        WHERE id = %s AND channel = %s AND channel_id = %s;
                    """
    cursor.execute(check_command,(id,channel, channel_id))
    row = cursor.fetchone()
    if row == None:
        return False
    return True

def delete_bookmark(id,channel,channel_id):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    #check if bookmark already exists
    check_command = """ DELETE FROM bookmarks
                        WHERE id = %s AND channel = %s AND channel_id = %s;
                    """
    cursor.execute(check_command,(id,channel,channel_id))
    conn.commit()
    conn.close()
    return

def get_bookmarks(id):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    #check if bookmark already exists
    check_command = """ SELECT * FROM bookmarks
                        WHERE id = %s;
                    """
    cursor.execute(check_command,(id,))
    bookmarks = cursor.fetchall()
    conn.commit()
    conn.close()
    return bookmarks


def bookmark_channel(id,channel,channel_id):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    #check if bookmark already exists
    check_command = """ SELECT * FROM bookmarks
                        WHERE id = %s AND channel = %s AND channel_id = %s;
                    """
    cursor.execute(check_command,(id,channel,channel_id))
    row = cursor.fetchone()
    if row != None:
        sys.stderr.write("aborted")
        return False #bookmark already exists, abort
    #otherwise, insert into the bookmarks table
    bookmark_command = """ INSERT INTO bookmarks(id, channel, channel_id)
                           VALUES (%s,%s,%s);
                        """
    cursor.execute(bookmark_command,(id,channel, channel_id))
    cursor.execute("SELECT * FROM bookmarks")#Testing Code
    test = str(cursor.fetchall()) #testing
    sys.stderr.write(test)#testing
    conn.commit()
    conn.close()
    return True #returns true for successful bookmark

#can change username paramerter to id if need be
def change_pass(username,new_password):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    hashed_new_pass = generate_password_hash(new_password,method="sha256")
    change_pass_command = """ UPDATE users 
                            SET password = %s
                            WHERE username = %s;
                          
                          """
    cursor.execute(change_pass_command,(hashed_new_pass,username))
    conn.commit()
    conn.close()

def get_password_by_username(username):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    password_check = """SELECT * FROM users
                    WHERE username = %s;
                """
    cursor.execute(password_check,(username,))
    row = cursor.fetchone()
    if row == None:
        return False
    conn.commit()
    conn.close()
    return row[3]

#save id into database
def name_to_id(channel_id, channel_name):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    insert_relation_command = """INSERT INTO idtoname(channel_id, channel_name)
                                VALUES(%s, %s);
                                """
    cursor.execute(insert_relation_command,(channel_id,channel_name))
    conn.commit()
    conn.close()

#get id from querying username
#returns id
def get_channel_id(channel_name):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    get_id_command = """SELECT channel_id FROM idtoname
                        WHERE channel_name = %s;
                    """
    cursor.execute(get_id_command,(channel_name,))
    retval = cursor.fetchone()
    return retval
