from systemapp import app
from flask import render_template

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