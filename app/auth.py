from flask import *
from . import db

auth = Blueprint('auth', __name__)

@auth.route("/login", methods =['POST', 'GET'])
def login():
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in fake_database:
            if user['username'] == username and user['password'] == password:
                authenticate(username,password)
                return redirect('/')
    """
    return render_template("Login.html")


@auth.route("/signup", methods=['POST','GET'])
def database_test():
    """
    import psycopg2
    db_config = os.environ['DATABASE_URL']
    print(db_config)
    conn = psycopg2.connect(db_config, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS test (food TEXT, rating INTEGER);")
    cursor.execute("INSERT INTO test VALUES ('borgir', 9);")
    cursor.execute("INSERT INTO test VALUES ('salad', 0);")
    conn.commit()
    cursor.execute("SELECT * FROM test;")
    rows = str(cursor.fetchall())
    sys.stderr.write(rows)
    conn.close()
    
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        print(email, username, password1, password2)
        if password1 == password2:
            for user in fake_database:
                if user['username'] == username:
                    return render_template("Signup.html")
            fake_database.append({'email': email,'username':username,'password':password1})
            return redirect('/')
    """
    return render_template("Signup.html")

#@app.route("/signup")