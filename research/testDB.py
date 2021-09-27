import sqlite3

def figma():
    conn = sqlite3.connect("testDB.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test (food TEXT, rating INTEGER)")
    cursor.execute("INSERT INTO test VALUES ('borgir', 9)")
    cursor.execute("INSERT INTO test VALUES ('salad', 0)")
    conn.commit()
    rows = cursor.execute("SELECT * FROM test").fetchall()
    print(rows)
    conn.close()

if __name__ == "__main__":
    figma()