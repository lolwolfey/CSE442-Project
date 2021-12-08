import sqlite3
#from sqlite3.dbapi2 import Cursor
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
import sys
#from ..database_handler import login_user,signup_user,bookmark_channel
#conn = sqlite3.connect("test.db")
#cur = conn.cursor
def local_initialize():
    #db.create_all()
    #RAW SQL
    #db_config = os.environ['DATABASE_URL']
    conn = sqlite3.connect("tests/testing.db")
    cursor = conn.cursor()
    #cursor.execute("DROP TABLE users")
    create_user_table = """CREATE TABLE IF NOT EXISTS users( 
                        id INTEGER,
                        email TEXT NOT NULL,
                        username VARCHAR(100) NOT NULL,
                        password VARCHAR(100) NOT NULL,
                        PRIMARY KEY (id),
                        UNIQUE (email,username)
                        );
                        """
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

def local_login_user(username,password):
    #db_config = os.environ['DATABASE_URL']
    conn = sqlite3.connect("tests/testing.db")
    cursor = conn.cursor()
    #look for same username in table
    login_command ="""SELECT * FROM users
                    WHERE username = ?;
                    """
    cursor.execute(login_command,(username,))
    row = cursor.fetchone()
    print(row)
    #then check if password is correct
    db_password = row[3]
    if row == None or not check_password_hash(db_password, password):
        return False
    #conn.commit()
    conn.close()
    return True

def local_signup_user(email,username,password):
    #db_config = os.environ['DATABASE_URL']
    conn = sqlite3.connect("tests/testing.db")
    cursor = conn.cursor()
    #check if email already exists
    email_check = """SELECT * FROM users
                     WHERE email = ?;
                """
    
    #check if username exists
    username_check = """SELECT * FROM users
                        WHERE username = ?;
                    """
    cursor.execute(email_check,(email,))
    returnemail = cursor.fetchone()
    print(returnemail)
    cursor.execute(username_check,(username,))
    returnusername = cursor.fetchone()
    print(returnusername)
    #None = none found in query
    if returnemail == None and returnusername == None:
        print("this is true")
        insert_user = """INSERT INTO users(email,username,password)
                        VALUES (?,?,?);
                    """
        hashed_pass=generate_password_hash(password, method='sha256')
        cursor.execute(insert_user,(email,username,hashed_pass))
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        print(rows)
        conn.commit()
        conn.close()
        return True #signup good
    conn.commit()
    conn.close()
    return False #signup failed

def local_bookmark_channel(id,channel):
    #db_config = os.environ['DATABASE_URL']
    conn = sqlite3.connect("tests/testing.db")
    cursor = conn.cursor()
    #check if bookmark already exists
    check_command = """ SELECT * FROM test_bm
                        WHERE id = ? AND channel = ?;
                    """
    cursor.execute(check_command,(id,channel))
    row = cursor.fetchone()
    if row != None:
        sys.stderr.write("aborted")
        return False #bookmark already exists, abort
    #otherwise, insert into the bookmarks table
    bookmark_command = """ INSERT INTO test_bm(id, channel)
                           VALUES (?,?);
                        """
    cursor.execute(bookmark_command,(id,channel))
    cursor.execute("SELECT * FROM test_bm")#Testing Code
    test = str(cursor.fetchall()) #testing
    sys.stderr.write(test)#testing
    conn.commit()
    conn.close()
    return True #returns true for successful bookmark

def local_change_pass(username,new_password):
    #db_config = os.environ['DATABASE_URL']
    conn = sqlite3.connect("tests/testing.db")
    cursor = conn.cursor()
    hashed_new_pass = generate_password_hash(new_password,method="sha256")
    change_pass_command = """ UPDATE users 
                            SET password = ?
                            WHERE username = ?;
                          
                          """
    cursor.execute(change_pass_command,(hashed_new_pass,username))
    conn.commit()
    conn.close()

def print_select_all():
    conn = sqlite3.connect("tests/testing.db")
    cursor = conn.cursor()
    command = "SELECT * FROM users"
    cursor.execute(command)
    print(cursor.fetchall())

def main():
    local_initialize()
    assert local_signup_user("hi@gmail.com","testuser","123456") == False
    #assert local_login_user("testuser", "123456") == True
    local_signup_user("hi2@liquid.com","matthewpatel","4561abc")
    local_bookmark_channel(1,"veritasium")
    assert local_bookmark_channel(1,"veritasium") == False
    print_select_all()
    local_change_pass("testuser","abc1548974549")
    print_select_all()
    assert local_login_user("testuser","abc1548974549") == True

if __name__ == '__main__':
    main()
