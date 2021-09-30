from flask import Flask
from flask import *
import os
app = Flask(__name__)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("Login.html")

def database_test():
    import psycopg2
    db_config = os.environ['DATABASE_URL']
    print(db_config)
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test (food TEXT, rating INTEGER)")
    cursor.execute("INSERT INTO test VALUES ('borgir', 9)")
    cursor.execute("INSERT INTO test VALUES ('salad', 0)")
    conn.commit()
    rows = cursor.execute("SELECT * FROM test").fetchall()
    print(rows)
    conn.close()
if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(host='0.0.0.0', port=port, debug=True)