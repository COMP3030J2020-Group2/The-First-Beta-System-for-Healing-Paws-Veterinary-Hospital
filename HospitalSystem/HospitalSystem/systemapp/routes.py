from systemapp import app,db
from flask import render_template, session, request, jsonify,redirect,url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from systemapp.forms import SignupForm, PetSignUpForm, LoginForm, PasswordForm, InformationForm, StaffLoginForm, QuestionForm
from systemapp.models import Customer, Pet, Staff, Question, Answer, Appointment
from datetime import datetime

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        customer = Customer.query.filter(Customer.email == form.email.data).first()
        if customer:
            return render_template('signup.html', title='Register a new user',form=form, emailerror = "Email already been used by other people")

        customer = Customer.query.filter(Customer.username == form.username.data).first()
        if customer:
            return render_template('signup.html', title='Register a new user',form=form, usernameerror = "Username already been used by other people")

        passw_hash = generate_password_hash(form.password.data)
        customer = Customer(username=form.username.data, email=form.email.data, password_hash=passw_hash)
        db.session.add(customer)
        db.session.commit()
        session["USERNAME"] = customer.username
        return render_template('customer_main.html')
    return render_template('signup.html', title='Register a new user', form=form)

@app.route('/pet_signup', methods=['GET', 'POST'])
def pet_signup():
    form = PetSignUpForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            customer = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            pet = Pet.query.filter(Pet.name == form.petname.data and Pet.owner_id == customer.id).first()
            if pet:
                return render_template('pet_signup.html', information='Same Name!', form=form)
            else:
                if form.type.data == 0:
                    return render_template('pet_signup.html', information='Choose a type', form=form)
                else:
                    new_pet = Pet(name=form.petname.data,type=form.type.data,owner = customer)
                    db.session.add(new_pet)
                    db.session.commit()
            return render_template('pet_signup.html', information='Successful!', form=form)
        return render_template('pet_signup.html', information='Register a new pet', form=form)
    else:
        return redirect(url_for('signup'))



@app.route('/checkuser', methods=['POST'])
def check_username():
    chosen_name = request.form['username']
    customer_in_db = Customer.query.filter(Customer.username == chosen_name).first()
    if not customer_in_db:
        return jsonify({'text': 'Username is available',
                        'returnvalue': 0})
    else:
        return jsonify({'text': 'Sorry! Username is already taken',
                        'returvalue': 1})


@app.route('/checkemail', methods=['POST'])
def check_email():
    chosen_email = request.form['email']
    email_in_db = Customer.query.filter(Customer.email == chosen_email).first()
    if not email_in_db:
        return jsonify({'text': 'Email is available',
                        'returnvalue': 0})
    else:
        return jsonify({'text': 'Sorry! Email is already taken',
                        'returvalue': 1})

@app.route('/customer_base')
def customer_base():
    return render_template('customer_base.html')


@app.route('/customer_main')
def customer_main():
    if not session.get("USERNAME") is None:
        customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
    return render_template('customer_main.html', user=customer_in_db, title='My Healing Paws')


@app.route('/customer_appointments',methods = ['GET'])
def customer_appointments():
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            #pets = user.pets
            pets = Pet.query.filter(Pet.owner_id == user.id)

            appointments = Appointment.query.filter(Appointment.pet_id == Pet.id)

    return render_template('customer_appointments.html', user=user, pets=pets, appointments=appointments)

@app.route('/customer_appointments/update_appointments/<id>',methods = ['GET', 'POST'])
def update_appointments(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appointment = db.session.query(Appointment).filter_by(id = id).first()
            return render_template('update_appointments.html',appointment = appointment)
        else:
            appointment_type = request.form['type']
            appointment_time = request.form['time1']
            appointment_description = request.form['description']
            appointment_pet_id = request.form['pet_id']
            appointment = Appointment.query.filter_by(id=id).update({'type': appointment_type, 'time': datetime.utcnow(), 'description': appointment_description, 'pet_id': appointment_pet_id})
            db.session.commit()
            return redirect('/customer_appointments')
    else:
        return redirect(url_for('index'))


@app.route('/customer_appointments/delete_appointment/<id>',methods = ['GET', 'POST'])
def delete_appointment(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            appointment = db.session.query(Appointment).filter_by(id=id).first()
            return render_template('delete_appointment.html', appointment=appointment)
        else:
             db.session.query(Appointment).filter_by(id = id).delete()
             db.session.commit()
             return redirect('/customer_appointments')
    else:
        return redirect(url_for('index'))


@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if not session.get("USERNAME") is None:
        customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        return render_template('customer_main.html', user=customer_in_db)
    else:
        form = LoginForm()
        if form.validate_on_submit():
            customer_in_db = Customer.query.filter(Customer.username == form.username.data).first()
            if not customer_in_db:
                return render_template('customer_login.html', title="Login as Customer", form=form, noneerror=" No such user. Register please")
            if check_password_hash(customer_in_db.password_hash, form.password.data):
                session["USERNAME"] = customer_in_db.username
                return render_template('customer_main.html', user=customer_in_db)
            else:
                return render_template('customer_login.html', title="Login as Customer", form=form, pwerror="Password incorrect!")
        return render_template('customer_login.html', title="Login as Customer", form=form)
    
    
@app.route('/customer_logout')
def customer_logout():
    session.pop("USERNAME", None)
    return redirect(url_for('index'))


@app.route('/personal_information',methods = ['GET'])
def personal_information():
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            pets=user.pets
            return render_template('personal_information.html',user=user,pets=pets)
    else:
        return redirect(url_for('customer_login'))


@app.route('/personal_information/update',methods = ['GET', 'POST'])
def update_information():
    if not session.get("USERNAME") is None:
        form = InformationForm()
        user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        if form.validate_on_submit():
            customer = Customer.query.filter(Customer.email == form.email.data).first()

            if customer:
                if customer.email != user.email:
                    return render_template('update_information.html', form=form, emailerror = "Email already been used by other people")

            customer = Customer.query.filter(Customer.username == form.username.data).first()
            if customer:
                if customer.username != user.username:
                    return render_template('update_information.html', form=form, usernameerror = "Username already been used by other people")

            update = Customer.query.filter(Customer.username == session.get("USERNAME")).update({'username':form.username.data,'email':form.email.data})
            db.session.commit()
            newone=Customer.query.filter(Customer.username == form.username.data).first()
            session["USERNAME"] = newone.username
            return redirect('/personal_information')
        else:
            return render_template('update_information.html', form=form, email = user.email, username=user.username)
    else:
        return redirect(url_for('customer_login'))




@app.route('/personal_information/check_password',methods = ['GET', 'POST'])
def check_password():
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            return render_template('password_check.html')
        else:
            password = request.form['password']
            user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            if (check_password_hash(user.password_hash, password)):
                return redirect(url_for('change_password'))
            flash('Incorrect Password')
            return redirect(url_for('check_password'))
    else:
        return redirect(url_for('customer_login'))

@app.route('/personal_information/change_password',methods = ['GET', 'POST'])
def change_password():
    if not session.get("USERNAME") is None:
        form = PasswordForm()
        if form.validate_on_submit():
            passw_hash = generate_password_hash(form.password.data)
            user = Customer.query.filter(Customer.username == session.get("USERNAME")).update({'password_hash':passw_hash})
            db.session.commit()
            user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            pets=user.pets
            return render_template('personal_information.html', user = user, pets = pets)
        return render_template('password_change.html', form=form)
    else:
        return redirect(url_for('customer_login'))

@app.route('/personal_information/update_pet/<id>',methods = ['GET', 'POST'])
def update_pet(id):
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            pet = Pet.query.filter_by(id = id).first()
            return render_template('update_pet.html',pet = pet)
        else:
            pet_name = request.form['name']
            pet_type = request.form['type']
            pet = Pet.query.filter_by(id = id).update({'name':pet_name, 'type':pet_type})
            db.session.commit()
            return redirect('/personal_information')
    else:
        return redirect(url_for('customer_login'))


@app.route('/personal_information/delete_pet/<id>')
def delete_pet(id):
    if not session.get("USERNAME") is None:
            pet = Pet.query.filter_by(id = id).delete()
            db.session.commit()
            return redirect('/personal_information')
    else:
        return redirect(url_for('customer_login'))


@app.route('/staff_login', methods=['GET','POST'])
def staff_login():
    form = StaffLoginForm()
    if form.validate_on_submit():
        staff_in_db = Staff.query.filter(Staff.name == form.staffname.data).first()
        if not staff_in_db:
            return render_template('staff_login.html',title="Control System Login",form=form, noneerror=" No such staff, please check your name.")
        if check_password_hash(staff_in_db.password_hash, form.password.data):
            session["STAFF"] = staff_in_db.name
            update_staff = Staff.query.filter(Staff.id == staff_in_db.id).update({"last_login":datetime.utcnow()})
            return render_template('control_system.html',staff = staff_in_db)
        else:
            return render_template('staff_login.html',title="Control System Login",form=form, pwerror="Password incorrect!")
    return render_template('staff_login.html',title="Control System Login",form=form)

@app.route('/control_system',methods=['GET','POST'])
def control_system():
    if not session.get("STAFF") is None:
        return redirect(url_for('staff_login'))
    else:
        staff = Staff.query.filter(Staff.name == session.get("STAFF"))
        return render_template('control_system.html',staff = staff)


@app.route('/customer_questions')
def customer_questions():
    if not session.get("USERNAME") is None:
        customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        questions=customer_in_db.questions.all()

        answered_questions=[]
        for question in questions:
            if question.answer.all():
                answered_questions.append(question)

        unanswered_questions=customer_in_db.questions.filter(Question.answer == None).all()

        return render_template('customer_questions.html', user=customer_in_db, unanswered_questions=unanswered_questions, answered_questions=answered_questions)
    else:
        return redirect(url_for('customer_login'))


@app.route('/create_questions',methods=['GET','POST'])
def create_questions():
    form = QuestionForm()
    if not session.get("USERNAME") is None:
        customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()

        if form.validate_on_submit():
            question = Question(title=form.title.data, content=form.content.data, questioner=customer_in_db)
            db.session.add(question)

            db.session.commit()

            return redirect(url_for('customer_questions'))
        return render_template('question_create.html', user=customer_in_db, form=form)
    else:
        return redirect(url_for('customer_login'))