from flask import *
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid Ussername or Password. Try Again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        redirect(url_for('main.home'))
    return render_template("Login.html")


@auth.route("/signup", methods=['POST','GET'])
def signup():
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
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 == password2:
            db.create_all()

            # Check to see if email already exists.
            user = User.query.filter_by(email=email).first()
            if user:
                flash('That email already exists')
                return redirect(url_for('auth.signup'))
            user = User.query.filter_by(email=email).first()

            # check to see if username already exists.
            if user:
                flash('That username already exists')
                return redirect(url_for('auth.signup'))
            
            # If the user does not exist and the passwords match, a new user is created.
            new_user = User(email=email, 
                            username=username, 
                            password=generate_password_hash(password1, method='sha256')
                            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))
        # Check to see if passwords match
        else:
            flash("Passwords do not match.")
            return redirect(url_for('auth.signup'))
        

        


    return render_template("Signup.html")

#@app.route("/signup")