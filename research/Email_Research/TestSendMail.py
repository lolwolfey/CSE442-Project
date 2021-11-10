"""
https://pythonbasics.org/flask-mail/
    - Tutorial on how to use flask-mail

https://pythonhosted.org/Flask-Mail/
    - Documentation
"""


from flask import Flask, render_template,request

from flask_mail import Mail, Message

app = Flask(__name__)


app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'redlomansmurf125@gmail.com',
	MAIL_PASSWORD = 'temp_pass'
	)

mail = Mail(app)


@app.route('/')
def index():
    return render_template("Mail.html")

@app.route('/send_mail', methods=["GET","POST"])
def send_message():
    if request.method == "POST":
        email = request.form['email']
        subject = "Password Change"
        
        message = Message(subject,sender="redlomansmurf125@gmail.com", recipients=[email])

        message.body = "message"

        mail.send(message)

        return "sent"

if __name__ == "__main__":
    app.run(debug=True, port=8000)