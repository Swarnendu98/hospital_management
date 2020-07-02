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
    patient_name=db.Column(db.Text,nullable=False)

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


@app.route('/create_patient',methods=['GET','POST'])
def create_patient():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            patient_adhar = request.form['patient_adhar']
            patient_name = request.form['patient_name']
            patient_age = request.form['patient_age']
            patient_bed_type = request.form['patient_bed_type']
            patient_address = request.form['patient_address']
            patient_state = request.form['patient_state']
            patient_city = request.form['patient_city']

            new_patient = patient_data(patient_adhar=patient_adhar, patient_age=patient_age,
                                       patient_bed_type=patient_bed_type,
                                       patient_address=patient_address, patient_state=patient_state,
                                       patient_city=patient_city,patient_name=patient_name)
            db.session.add(new_patient)
            db.session.commit()
            message = 'Patient added Successfully'
            return render_template("create_patient.html",message=message)
        else:
            #all_patient = patient_data.query.order_by(patient_data.date_posted).all()
            return render_template('create_patient.html')

@app.route('/update_patient',methods=['GET','POST'])
def update_patient():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST' and 'search' in request.form:
            search = request.form.get('search')
            data= patient_data.query.filter_by(patient_adhar=search).first()
            if data is None:
                return render_template("update_patient.html",message="Patient does not exist")
            else:
                return render_template("update_patient.html",data = data )
        elif request.method =='POST' and 'patient_adhar' in request.form:
            patient_id =        request.form['patient_id']
            patient_adhar =     request.form['patient_adhar']
            patient_age =       request.form['patient_age']
            patient_bed_type =  request.form['patient_bed_type']
            patient_address =   request.form['patient_address']
            patient_state =     request.form['patient_state']
            patient_city =      request.form['patient_city']
            patient_name =      request.form['patient_name']

            update = patient_data.query.filter_by(patient_id = patient_id).first()

            update.patient_adhar = patient_adhar
            update.patient_age = patient_age
            update.patient_bed_type = patient_bed_type
            update.patient_address = patient_address
            update.patient_state = patient_state
            update.patient_city = patient_city
            update.patient_name = patient_name

            db.session.commit()

            return render_template("update_patient.html", message="Patient Updated")
        else:
            return render_template("update_patient.html")

@app.route('/delete_patient',methods=['GET','POST'])
def delete_patient():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST' and 'search' in request.form:
            search = request.form.get('search')
            data= patient_data.query.filter_by(patient_adhar=search).first()
            if data is None:
                return render_template("delete_patient.html",message="Patient does not exist")
            else:
                return render_template("delete_patient.html",data = data )


        elif request.method == 'POST' and 'patient_adhar' in request.form:
            patient_id =        request.form['patient_id']
            #HARD DELETE OPTION DUE TO NO patient_status FIELD IN DATABASE
            patient_data.query.filter_by(patient_id = patient_id).delete()
            db.session.commit()

            return render_template("delete_patient.html", message="Patient Deleted")
        else:
            return render_template("delete_patient.html")

@app.route('/show_record',methods=['GET','POST'])
def show_record():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        data = patient_data.query.all()
        return render_template('show_record.html',data=data)


@app.route('/add_meds',methods=['GET','POST'])
def add_meds():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method =='POST':
            patient_id=request.form['patient_id']
            medicine_name= request.form['medicine_name']
            quantity = request.form['quantity']
            price = request.form['price']

            new_medicine = pharmacy_data(patient_id=patient_id,medicine_name=medicine_name,quantity=quantity,price=price)
            db.session.add(new_medicine)
            db.session.commit()
            message = 'medicine added'
            return render_template('add_meds.html',message=message)
        else:
            return render_template('add_meds.html')
@app.route('/show_meds_record',methods=['GET','POST'])
def show_meds_record():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST' and 'search' in request.form:
            search = request.form.get('search')
            data= pharmacy_data.query.filter_by(patient_id=search)
            if data is None:
                return render_template('show_meds_record.html',message="Patient does not exist")
            else:
                return render_template('show_meds_record.html',data = data )
        else:
            return render_template('show_meds_record.html')


@app.route('/add_diagnosis',methods=['GET','POST'])
def add_diagnosis():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method =='POST':
            patient_id=request.form['patient_id']
            test_name= request.form['test_name']
            cost = request.form['cost']

            new_diagnosis = diagnosis_data(patient_id=patient_id,test_name=test_name,cost=cost)
            db.session.add(new_diagnosis)
            db.session.commit()
            message = 'diagnosis added'
            return render_template('add_diagnosis.html',message=message)
        else:
            return render_template('add_diagnosis.html')













