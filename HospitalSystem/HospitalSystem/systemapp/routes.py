from systemapp import app,db
from flask import render_template, session, request, jsonify,redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from systemapp.forms import SignupForm,PetSignUpForm
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