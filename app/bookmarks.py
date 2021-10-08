import sys
import psycopg2
import os

def bookmark_channel(id,channel):
    db_config = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    #check if bookmark already exists
    check_command = """ SELECT * FROM bookmarks
                        WHERE id = %s AND channel = %s;
                    """
    cursor.execute(check_command,(id,channel))
    row = cursor.fetchone()
    if row != None:
        return False #bookmark already exists, abort
    #otherwise, insert into the bookmarks table
    bookmark_command = """ INSERT INTO bookmarks(id, channel)
                           VALUES (%s,%s);
                        """
    cursor.execute(bookmark_command,(id,channel))
    conn.commit()
    conn.close()
    return True #returns true for successful bookmark