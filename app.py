from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)

class executive_data(db.Model):
    ex_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ex_pass = db.Column(db.VARCHAR(25),nullable=False)
class patient_data(db.Model):
    patient_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    patient_adhar= db.Column(db.BigInteger,unique=True)
    patient_age= db.Column(db.Integer,nullable=False)
    patient_admission_date=db.Column(db.DateTime,nullable=False,default=date.today())
    patient_bed_type = db.Column(db.String,nullable=False)
    patient_address=db.Column(db.String,nullable=False)
    patient_state = db.Column(db.String,nullable=False)
    patient_city=db.Column(db.String,nullable=False)
class pharmacy_data(db.Model):
    pharmacy_bill_no = db.Column(db.Integer,primary_key=True,autoincrement=True)
    patient_id=db.Column(db.Integer,nullable=False)
    medicine_name=db.Column(db.String,nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Float,nullable=False)
class diagnosis_data(db.Model):
    diagnosis_bill_no=db.Column(db.Integer,primary_key=True,autoincrement=True)
    patient_id=db.Column(db.Integer,nullable=False)
    test_name=db.Column(db.String,nullable=False)
    cost =db.Column(db.Float,nullable=False)


    def __repr__(self):
        return 'details'+str(self.ex_id)

@app.route("/")
def login():
    return 'H'
