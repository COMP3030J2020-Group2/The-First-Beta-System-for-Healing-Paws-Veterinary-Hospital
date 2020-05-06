from systemapp import app,db
from flask import render_template, session, request, jsonify,redirect,url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from systemapp.forms import SignupForm, PetSignUpForm, LoginForm, PasswordForm, InformationForm, StaffLoginForm, QuestionForm, AppointmentForm, EmergencyAppointmentForm, StaffSignupForm, AnswerForm
from systemapp.models import Customer, Pet, Staff, Question, Answer, Appointment
from datetime import datetime
from sqlalchemy import or_,and_


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
        return redirect(url_for('customer_console_main'))
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
            return redirect(url_for('customer_my_pets'))
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


# @app.route('/customer_base')
# def customer_base():
#     return render_template('customer_base.html')


@app.route('/customer_console_base')
def customer_console_base():
    return render_template('customer_console_base.html')


@app.route('/customer_console_main', methods=['GET', 'POST'])
def customer_console_main():
    form = AppointmentForm()
    formEm = EmergencyAppointmentForm()
    customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
    pets = Pet.query.filter(Pet.owner_id == customer_in_db.id).all()
    pets_list = [(i.id, i.name) for i in pets]
    form.pets.choices = pets_list
    formEm.pets.choices = pets_list
    appointment_details=[]
    for p in pets:
        appointment_details.append(Appointment.query.filter(Appointment.pet_id == p.id).all())

    if form.validate_on_submit():
        pet_selected = request.form['pets']
        ongoing_appointment = Appointment.query.filter(and_(or_(Appointment.status==0, Appointment.status==1),Appointment.pet_id == pet_selected)).first()
        if not ongoing_appointment:
            appointment = Appointment(description=form.description.data, type=1, hospital_location = form.location.data, pet_id=pet_selected)
            db.session.add(appointment)
            db.session.commit()
        else:
            flash("This pet has on going appointment already!")
            return redirect(url_for('customer_console_main'))
        return redirect(url_for('customer_console_main'))
    if formEm.validate_on_submit():
        pet_selected = request.form['pets']
        ongoing_appointment = Appointment.query.filter(and_(or_(Appointment.status==0, Appointment.status==1),Appointment.pet_id == pet_selected)).first()
        if not ongoing_appointment:
            appointment = Appointment(description="Emergency Appointment, please prepare!", type=0,hospital_location = form.location.data, pet_id=pet_selected)
            db.session.add(appointment)
            db.session.commit()
        else:
            flash("This pet has on going appointment already!")
            return redirect(url_for('customer_console_main'))
        return redirect(url_for('customer_console_main'))
    return render_template('customer_console_main.html', user=customer_in_db, title='My Healing Paws', form=form, form0=formEm,
                           appointment_details=appointment_details)


# @app.route('/customer_main', methods=['GET', 'POST'])
# def customer_main():
#     form = AppointmentForm()
#     formEm = EmergencyAppointmentForm()
#     customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
#     pets = Pet.query.filter(Pet.owner_id == customer_in_db.id).all()
#     pets_list = [(i.id, i.name) for i in pets]
#     form.pets.choices = pets_list
#     formEm.pets.choices = pets_list
#     if form.validate_on_submit():
#         pet_selected = request.form['pets']
#         appointment = Appointment(description=form.description.data, type=1, pet_id=pet_selected)
#         db.session.add(appointment)
#         db.session.commit()
#         return redirect(url_for('customer_main'))
#     if formEm.validate_on_submit():
#         pet_selected = request.form['pets']
#         appointment = Appointment(description="Emergency Appointment, please prepare!", type=0, pet_id=pet_selected)
#         db.session.add(appointment)
#         db.session.commit()
#         return redirect(url_for('customer_main'))
#     return render_template('customer_main.html', user=customer_in_db, title='My Healing Paws', form=form, form0=formEm)


@app.route('/customer_appointments',methods = ['GET'])
def customer_appointments():
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            #pets = user.pets
            pets = Pet.query.filter(Pet.owner_id == user.id)

            appointments = Appointment.query.filter(Appointment.pet_id == Pet.id)

    return render_template('customer_appointments.html', user=user, pets=pets, appointments=appointments)

@app.route('/update_appointments/<id>',methods = ['GET', 'POST'])
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


@app.route('/delete_appointment/<id>',methods = ['GET', 'POST'])
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
        # return render_template('customer_main.html', user=customer_in_db)
        return redirect(url_for('customer_console_main'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            customer_in_db = Customer.query.filter(Customer.username == form.username.data).first()
            if not customer_in_db:
                return render_template('customer_login.html', title="Login as Customer", form=form, noneerror=" No such user. Register please")
            if check_password_hash(customer_in_db.password_hash, form.password.data):
                session["USERNAME"] = customer_in_db.username
                # return render_template('customer_main.html', user=customer_in_db)
                return redirect(url_for('customer_console_main'))
            else:
                return render_template('customer_login.html', title="Login as Customer", form=form, pwerror="Password incorrect!")
        return render_template('customer_login.html', title="Login as Customer", form=form)
    
    
@app.route('/customer_logout')
def customer_logout():
    session.pop("USERNAME", None)
    return redirect(url_for('index'))


@app.route('/customer_profile',methods = ['GET'])
def customer_profile():
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
            return redirect('/customer_profile')
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

@app.route('/update_pet/<id>',methods = ['GET', 'POST'])
def update_pet(id):
    form = PetSignUpForm()
    pet = Pet.query.filter_by(id = id).first()

    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            customer = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            a_pet = Pet.query.filter(Pet.name == form.petname.data and Pet.owner_id == customer.id).first()
            if a_pet:
                if pet is not a_pet:
                    return render_template('pet_signup.html', information='Same name with your another pet!', form=form)
            else:
                if form.type.data == 0:
                    return render_template('pet_signup.html', information='Choose a type', form=form)
                else:
                    pet = Pet.query.filter_by(id = id).update({'name':form.petname.data, 'type':form.type.data})
                    db.session.commit()
            return redirect(url_for('customer_my_pets'))
        form.petname.data=pet.name
        form.type.data=pet.type
        return render_template('pet_signup.html', information='Edit your pet information' , form=form)
    else:
        return redirect(url_for('customer_login'))


@app.route('/delete_pet/<id>')
def delete_pet(id):
    if not session.get("USERNAME") is None:
            pet = Pet.query.filter_by(id = id).delete()
            db.session.commit()
            return redirect('/customer_console_main/my_pets')
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
            return redirect(url_for('control_system'))
        else:
            return render_template('staff_login.html',title="Control System Login",form=form, pwerror="Password incorrect!")
    return render_template('staff_login.html',title="Control System Login",form=form)

@app.route('/control_system',methods=['GET','POST'])
def control_system():
    if not session.get("STAFF"):
        return redirect(url_for('staff_login'))
    else:
        staff = Staff.query.filter(Staff.name == session.get("STAFF")).first()
        return render_template('control_system.html',staff = staff)



@app.route('/staff_check_appointments/on_going',methods=['GET','POST'])
def on_going():
    ongoing_appoints = Appointment.query.filter(Appointment.status == 0).all()
    customer_list = []
    pet_list = []
    for appoint in ongoing_appoints:
        pet = Pet.query.filter(Pet.id == appoint.pet_id).first()
        customer = Customer.query.filter(Customer.id == pet.owner_id).first()
        customer_list.append(customer.username)
        pet_list.append(pet)

    if request.method == 'GET':
        list_ongoing_appoints=list(enumerate(ongoing_appoints))
        return render_template('staff_check_appointments.html',appoints = list_ongoing_appoints,appointment  = 'On Going', 
            button = 'Finish',class_on_going = "nav-link active", class_unchecked = "nav-link", class_finished = "nav-link",button_style="btn btn-primary", pets=pet_list,customers=customer_list)
    else:
        data = request.form.to_dict()
        rowIndex = data.get('id')
        appointment = Appointment.query.filter(Appointment.id == rowIndex).first()
        buttonType = data.get('buttonType')
        if buttonType == "Finish":
            appointment.status = 2
            appointment.pet_status = "Released"
        elif buttonType == "Take in":
            appointment.pet_status = "Was Taken"
        elif buttonType == "Complete Surgery":
            appointment.pet_status = "Surgery Completed"
        elif buttonType == "Inform Customer for Releasing":
            appointment.pet_status = "Ready for release"
        elif buttonType == "Confirm Surgery Date":
            meeting_date =  data.get('meetingDate')
            appointment.surgery_date = datetime.strptime(meeting_date, "%Y-%m-%d %H:%M")
            appointment.pet_status = "Surgery Date Confirmed"

        db.session.commit()
        return redirect(url_for('on_going'))

@app.route('/staff_check_appointments/unchecked',methods=['GET','POST'])
def unchecked():
    unchecked_appoints = Appointment.query.filter(Appointment.status == 1).all()
    customer_list = []
    pet_list = []
    for appoint in unchecked_appoints:
        pet = Pet.query.filter(Pet.id == appoint.pet_id).first()
        customer = Customer.query.filter(Customer.id == pet.owner_id).first()
        customer_list.append(customer.username)
        pet_list.append(pet)

    if request.method == 'GET':
        list_unchecked_appoints=list(enumerate(unchecked_appoints))
        return render_template('staff_check_appointments.html',appoints = list_unchecked_appoints,appointment = 'Unchecked', 
            button = 'Check',class_on_going = "nav-link", class_unchecked = "nav-link active", class_finished = "nav-link",button_style="btn btn-success",pets=pet_list,customers=customer_list)
    else:
        data = request.form.to_dict()
        rowIndex = data.get('id')
        meeting_date =  data.get('meetingDate')
        appointment = Appointment.query.filter(Appointment.id == rowIndex).first()
        appointment.status = 0
        print(meeting_date)
        appointment.meeting_date = datetime.strptime(meeting_date, "%Y-%m-%d %H:%M")
        db.session.commit()
        return redirect(url_for('unchecked'))

@app.route('/staff_check_appointments/finished',methods=['GET','POST'])
def finished():
    finished_appoints = Appointment.query.filter(Appointment.status == 2).all()
    customer_list = []
    pet_list = []
    for appoint in finished_appoints:
        pet = Pet.query.filter(Pet.id == appoint.pet_id).first()
        customer = Customer.query.filter(Customer.id == pet.owner_id).first()
        customer_list.append(customer.username)
        pet_list.append(pet)
    if request.method == 'GET':
        list_finished_appoints=list(enumerate(finished_appoints))
        return render_template('staff_check_appointments.html',appoints = list_finished_appoints,appointment  = 'Finished', 
            button = 'Active',class_on_going = "nav-link", class_unchecked = "nav-link", class_finished = "nav-link active",button_style="btn btn-secondary",pets=pet_list,customers=customer_list)
    else:
        data = request.form.to_dict()
        rowIndex = data.get('id')
        appointment = Appointment.query.filter(Appointment.id == rowIndex).first()
        appointment.status = 0
        db.session.commit()
        return redirect(url_for('finished'))

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


@app.route('/customer_questions/<id>',methods = ['GET', 'POST'])
def customer_questiondetail(id):
    if not session.get("USERNAME") is None:
        user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        question = Question.query.filter_by(id = id).first()
        answer=question.answer.all()
        return render_template('customer_questiondetail.html',question = question, answer=answer, user=user)
    else:
        return redirect(url_for('customer_login'))


@app.route('/edit_question/<id>',methods = ['GET', 'POST'])
def edit_question(id):
    form = QuestionForm()
    if not session.get("USERNAME") is None:
        customer_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        question = Question.query.filter_by(id = id).first()
        if form.validate_on_submit():
            update = Question.query.filter_by(id = id).update({'title':form.title.data,'content':form.content.data})
            db.session.commit()
            return redirect(url_for('customer_questiondetail',id=id))
        return render_template('customer_question_update.html', user=customer_in_db, form=form, qtitle = question.title, qcontent = question.content)
    else:
        return redirect(url_for('customer_login'))


@app.route('/customer_questions/delete_question/<id>')
def delete_question(id):
    if not session.get("USERNAME") is None:
        user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        question = Question.query.filter_by(id = id).first()
        answer=question.answer.delete()
        remove = Question.query.filter_by(id = id).delete()
        db.session.commit()
        return redirect('/customer_questions')
    else:
        return redirect(url_for('customer_login'))




@app.route('/check_appointment/<id>',methods=['GET','POST'])
def check_appointment(id):
    if not session.get("STAFF"):
        return redirect(url_for('staff_login'))
    else:
        apm_in_db = Appointment.query.filter(Appointment.id == id).first()
        pet = Pet.query.filter(Pet.id == apm_in_db.pet_id).first()
        customer = Customer.query.filter(Customer.id == pet.owner_id).first()
        if not apm_in_db:
            return redirect(url_for('control_system'))
        return render_template('staff_operate_appointment.html', appointment=apm_in_db, pet = pet, customer = customer)

@app.route('/check_pet/<id>',methods=['GET','POST'])
def check_pet(id):
    if not session.get("STAFF"):
        return redirect(url_for('staff_login'))
    else:
        pet_in_db = Pet.query.filter(Pet.id == id).first()
        owner = Customer.query.filter(Customer.id == pet_in_db.owner).first()
        if not pet_in_db:
            return redirect(url_for('control_system'))
        return render_template('staff_check_pet.html',pet=pet_in_db,owner=owner)

@app.route('/appointment_ongoing/<id>',methods=['GET','POST'])
def appointment_ongoing(id):
    if not session.get("STAFF"):
        return redirect(url_for('staff_login'))
    else:
        staff_in_db = Staff.query.filter(Staff.name == session.get("STAFF")).first()
        if staff_in_db.level < 3:
            return redirect('control_system') #staff level
    apm_in_db = Appointment.query.filter(Appointment.id == id).first()
    if apm_in_db:
        apm_in_db = Appointment.query.filter_by(id = id).update({"status":0})
        return redirect(url_for('on_going'))
    else:
        return redirect(url_for('control_system'))

@app.route('/appointment_finish/<id>',methods=['GET','POST'])
def appointment_finish(id):
    if not session.get("STAFF"):
        return redirect(url_for('staff_login'))
    else:
        staff_in_db = Staff.query.filter(Staff.name == session.get("STAFF")).first()
        if staff_in_db.level < 3:
            return redirect('control_system') #staff level
    apm_in_db = Appointment.query.filter(Appointment.id == id).first()
    if apm_in_db:
        apm_in_db = Appointment.query.filter_by(id = id).update({"status":2})
        return redirect(url_for('finished'))
    else:
        return redirect(url_for('control_system'))



@app.route('/staffsignup', methods=['GET', 'POST'])
def staffsignup():
    form = StaffSignupForm()
    if form.validate_on_submit():
        staff = Staff.query.filter(Staff.name == form.staffname.data).first()
        if staff:
            return render_template('staff_signup_fortest.html', title='Register a new user',form=form)

        passw_hash = generate_password_hash(form.password.data)
        int_level = int(form.level.data)
        staff = Staff(name=form.staffname.data, level=int_level, password_hash=passw_hash)
        db.session.add(staff)
        db.session.commit()
        session["STAFF"] = staff.name
        return render_template('control_system.html' ,staff = staff)
    return render_template('staff_signup_fortest.html', title='Register a new staff(test version)', form=form)

@app.route('/staff_search/<query>',methods=['GET','POST'])
def staff_search(query):
    if not session.get("STAFF"):
        return redirect(url_for('staff_login'))
    if query.isnumeric():
        id = int(query)
        apm_in_db = Appointment.query.filter(Appointment.id == id).first()
        customer_in_db = Customer.query.filter(Customer.id == id).first()
        return render_template('staff_search.html',apm = apm_in_db , customer = customer_in_db, query = query)
    else:
        apm_list = Appointment.query.filter(Appointment.description.like('%'+query+'%')).all()
        customer_list = Customer.query.filter(Customer.username.like('%'+query+'%')).all()
        return render_template('staff_search.html',apmlist = apm_list, customerlist = customer_list, query = query)


@app.route('/customer_console_main/my_pets', methods=['GET', 'POST'])
def customer_my_pets():
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            customer = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            pets = Pet.query.filter(Pet.owner_id == customer.id).all()
            return render_template('customer_mypets.html',pets=pets,user=customer)
        else:
            data = request.form.to_dict()
            id = data.get("id");
            pet = Pet.query.filter(Pet.id == id).first()
            return render_template('pet_information.html',pet=pet)
    else:
        return redirect(url_for('login'))

@app.route('/staff_questions')
def staff_questions():
    if not session.get("STAFF") is None:
        staff = Staff.query.filter(Staff.name == session.get("STAFF")).first()
        questions=Question.query.all()

        answered_questions=[]
        for question in questions:
            if question.answer.all():
                answered_questions.append(question)

        unanswered_questions=Question.query.filter(Question.answer == None).all()

        return render_template('staff_questions.html', unanswered_questions=unanswered_questions, answered_questions=answered_questions)
    else:
        return redirect(url_for('staff_login'))

@app.route('/staff_questions/<id>',methods = ['GET', 'POST'])
def staff_questiondetail(id):
    if not session.get("STAFF") is None:
        question = Question.query.filter_by(id = id).first()
        answer=question.answer.all()
        return render_template('staff_questiondetail.html',question = question, answer=answer)
    else:
        return redirect(url_for('staff_login'))


@app.route('/staff_questions/answer_question/<id>',methods = ['GET', 'POST'])
def answer_question(id):
    form = AnswerForm()
    if not session.get("STAFF") is None:
        staff = Staff.query.filter(Staff.name == session.get("STAFF")).first()
        question = Question.query.filter_by(id = id).first()
        if form.validate_on_submit():
            answer = Answer(content=form.content.data, question=question, respondent=staff)
            db.session.add(answer)
            db.session.commit()
            return redirect(url_for('staff_questions'))
        return render_template('answer_question.html',question = question, form=form)
    else:
        return redirect(url_for('staff_login'))

@app.route('/staff_questions/edit_answer/<id>',methods = ['GET', 'POST'])
def edit_answer(id):
    form = AnswerForm()
    if not session.get("STAFF") is None:
        staff = Staff.query.filter(Staff.name == session.get("STAFF")).first()
        answer = Answer.query.filter_by(id = id).first()
        question=answer.question
        if form.validate_on_submit():
            update = Answer.query.filter_by(id = id).update({'content':form.content.data})
            db.session.commit()
            return redirect(url_for('staff_questiondetail',id=question.id))
        return render_template('answer_question.html', form=form, question=question, content = answer.content)
    else:
        return redirect(url_for('staff_login'))


@app.route('/staff_questions/delete_answer/<id>')
def delete_answer(id):
    if not session.get("STAFF") is None:
        staff = Staff.query.filter(Staff.name == session.get("STAFF")).first()
        answer = Answer.query.filter_by(id = id).first()
        question=answer.question
        remove = Answer.query.filter_by(id = id).delete()
        db.session.commit()
        return redirect(url_for('staff_questiondetail',id=question.id))
    else:
        return redirect(url_for('staff_login'))

@app.route('/staff_questions/delete/<id>')
def delete_QA(id):
    if not session.get("STAFF") is None:
        staff = Staff.query.filter(Staff.name == session.get("STAFF")).first()
        question = Question.query.filter_by(id = id).first()
        answer=question.answer.delete()
        remove = Question.query.filter_by(id = id).delete()
        db.session.commit()
        return redirect('/staff_questions')
    else:
        return redirect(url_for('staff_login'))





@app.route('/staff_checkpets',methods = ['GET', 'POST'])
def staff_checkpets():
    if not session.get("STAFF") is None:
        if request.method == 'GET':
            pets = Pet.query.filter().all()
            customers = Customer.query.filter(Customer.id == Pet.owner_id)
            appointments = Appointment.query.filter().all()
            return render_template('staff_checkpets.html',pets = pets,customers = customers,appointments=appointments)
    else:
        return redirect(url_for('staff_login'))


@app.route('/staff_checkpets/update_pet/<id>',methods = ['GET', 'POST'])
def staff_updatepet(id):
    if not session.get("STAFF") is None:
        if request.method == 'GET':
            pet = Pet.query.filter_by(id = id).first()
            return render_template('staff_updatepet.html',pet = pet)
        else:
            pet_name = request.form['name']
            pet_type = request.form['type']
            pet = Pet.query.filter_by(id = id).update({'name':pet_name, 'type':pet_type})
            db.session.commit()
            return redirect('/staff_checkpets')
    else:
        return redirect(url_for('staff_login'))
