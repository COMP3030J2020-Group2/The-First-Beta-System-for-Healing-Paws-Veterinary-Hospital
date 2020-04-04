from systemapp import app,db
from flask import render_template, session, request, jsonify,redirect,url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from systemapp.forms import SignupForm, PetSignUpForm, LoginForm, PasswordForm, InformationForm
from systemapp.models import Customer, Pet

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
        return render_template('after_login_page.html')
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


@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    form = LoginForm()
    if form.validate_on_submit():
        customer_in_db = Customer.query.filter(Customer.username == form.username.data).first()
        if not customer_in_db:
            return render_template('customer_login.html', title="Login as Customer", form=form, noneerror=" No such user. Register please")
        if check_password_hash(customer_in_db.password_hash, form.password.data):
            session["USERNAME"] = customer_in_db.username
            return render_template('after_login_page.html', user=customer_in_db)
        else:
            return render_template('customer_login.html', title="Login as Customer", form=form, pwerror="Password incorrect!")
    return render_template('customer_login.html', title="Login as Customer", form=form)



@app.route('/personal_information',methods = ['GET'])
def personal_information():
    if not session.get("USERNAME") is None:
        if request.method == 'GET':
            user = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            pets=user.pets
            return render_template('personal_information.html',user=user,pets=pets)


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
        return redirect(url_for('index'))




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
        return redirect(url_for('index'))

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
        return redirect(url_for('index'))

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
        return redirect(url_for('index'))


@app.route('/personal_information/delete_pet/<id>')
def delete_pet(id):
    if not session.get("USERNAME") is None:
            pet = Pet.query.filter_by(id = id).delete()
            db.session.commit()
            return redirect('/personal_information')
    else:
        return redirect(url_for('index'))
