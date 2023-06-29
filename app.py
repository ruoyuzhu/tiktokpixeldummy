from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy

#from flask_restful import Resource, Api
import sys
import os

app = Flask(__name__,template_folder='.')
port = 5100

if sys.argv.__len__() > 1:
    port = sys.argv[1]
print("Api running on port : {} ".format(port))

## define data model
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Add a secret key for session management

app.app_context()
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.email
app.app_context().push()

class Visits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(120), nullable=True)
    fbq_cookie = db.Column(db.String(120), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    user_agent = db.Column(db.String(500), nullable=False)
db.create_all()


@app.route("/")
def home():
    visit = Visits(
        session_id=session.get('session_id'),
        fbq_cookie=request.cookies.get("_fbp"), 
        ip_address=request.remote_addr,
        user_agent= request.user_agent.string
        )
    db.session.add(visit)
    db.session.commit()
    return render_template("index.html")

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['email'] = user.email  # Store user's email in the session
        return redirect("/")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
