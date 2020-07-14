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
    username = db.Column(db.String(20), nullable=False)
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

@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("Error")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    username_check = db.session.query(User.username).filter(User.username == username).first()
    if username_check is not None:
        return jsonify("Username taken")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf8")

    record = User(username, hashed_password)
    db.session.add(record)
    db.session.commit()

    return jsonify("User created")

@app.route("/appointment/add", methods=["POST"])
def add_appointment():
    if request.content_type != "application/json":
        return jsonify("Error")

    post_data = request.get_json()
    username = post_data.get("username")
    title = post_data.get("title")
    company = post_data.get("company")
    start_date = post_data.get("start_date")
    

    new_appointment = Appointment(username, title, company, start_date)
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify("Appointment added!")

@app.route("/appointment/get/data", methods=["GET"])
def get_appointment_data():
    appointment_data = db.session.query(Appointment).all()
    return jsonify(appointments_schema.dump(appointment_data))

@app.route("/appointment/get/data/<username>", methods=["GET"])
def get_all_appointments_by_username(username):
    appointment_data = db.session.query(Appointment).filter(Appointment.username == username).all()
    return jsonify(appointments_schema.dump(appointment_data))

if __name__ == "__main__":
    app.run(debug=True)