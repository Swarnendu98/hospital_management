from flask import Flask,render_template,request,g,session,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date



app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

class executive_data(db.Model):
    ex_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ex_pass = db.Column(db.VARCHAR(25),nullable=False)
    ex_name = db.Column(db.String,nullable=False)
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

@app.route("/",methods=['GET','POST'])
def login():
    if request.method =='POST' and 'ex_id' and 'ex_pass' in request.form:
        session.pop('user_id',None)
        ex_id= request.form.get('ex_id')
        ex_pass=request.form.get('ex_pass')
        password = executive_data.query.get(ex_id).ex_pass
        if password == ex_pass :
            session['user_id']= ex_id
            return redirect(url_for('home'))
        else:
            message = 'INCORRECT USER NAME OR PASSWORD'
            return render_template('login.html',message=message)
    else:
        return render_template('login.html')
@app.route("/home")
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        ex_id = session['user_id']
        ex_data = executive_data.query.get_or_404(ex_id)
        ex_name = ex_data.ex_name

        return render_template('home.html',name = ex_name)
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('user_id', None)
   return redirect(url_for('login'))

