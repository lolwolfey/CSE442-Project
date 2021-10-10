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
            if user[3] == generate_password_hash(password):
                self.email = user[1]
                self.username = user[2]
                self.hashedPassword = user[3]
                self.user_id = user[0]
                sys.stdout.write(user[0])
                sys.stdout.write(self.user_id)

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
    cursor.execute(delete_bookmarks_table)
    cursor.execute(delete_user_table)

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
    db_password = row[3]
    if row == None or not check_password_hash(db_password, password):
        return False
    conn.commit()
    conn.close()
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
    cursor.execute(email_check,(email,))
    returnemail = cursor.fetchone()
    cursor.execute(username_check,(username,))
    returnusername = cursor.fetchone()
    #None = none found in query
    if returnemail == None and returnusername == None:
        insert_user = """INSERT INTO users(email,username,password)
                        VALUES (%s,%s,%s);
                    """
        hashed_pass=generate_password_hash(password, method='sha256')
        cursor.execute(insert_user,(email,username,hashed_pass))
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