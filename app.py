from flask import Flask
from flask import *
import os
app = Flask(__name__)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("Login.html")

if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(host='0.0.0.0', port=port, debug=True)