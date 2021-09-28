import sqlite3

def register_user(username,password):
    '''
    register_user(string,string)
    validates whether or not the username is valid and not taken already
    checks if password is strong enough, hashes and salts it
    stores username and password in a DB
    if both are true, then this function will return true, else false
    '''
    return False

def login_user(username, password):
    '''
    login_user (string,string)
    validates if username exists
    checks if password is correct
    returns a boolean
    '''
    return False

def bookmark_user(username1, channel):
    '''
    username1 wants to bookmark a channel
    creates an entry in a table in a one -> many relationship
    returns true if the channel exists
    '''
    return False