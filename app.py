from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt
import io

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""

db = SQLAlchemy(app)
ma = Marshmallow(app)
heroku = Heroku(app)
CORS(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(), nullable=False)
    company = db.Column(db.String(), nullable=False)
    start_date = db.Column(db.String(), nullable=False)

    def __init__(self, username, title, company, start_date):
        self.username = username
        self.title = title
        self.company = company
        self.start_date = start_date
        
class AppointmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "title", "company", "start_date")

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)


if __name__ == "__main__":
    app.run(debug=True)