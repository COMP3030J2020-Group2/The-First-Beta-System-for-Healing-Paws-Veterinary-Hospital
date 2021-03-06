from systemapp import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    pets = db.relationship('Pet',backref='owner',lazy='dynamic')
    questions= db.relationship('Question',backref='questioner',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Staff(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name  = db.Column(db.String(64),index=True,unique=True)
    level = db.Column(db.Integer,index=True)
    password_hash = db.Column(db.String(128))
    last_login = db.Column(db.DateTime,index=True,default=datetime.utcnow())
    appointments = db.relationship('Appointment',backref='operator',lazy='dynamic')
    answers= db.relationship('Answer',backref='respondent',lazy='dynamic')

    def __repr__(self):
        return '<Staff {}>'.format(self.name)

class Pet(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),index=True,unique=True)
    type = db.Column(db.Integer,nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    appointments = db.relationship('Appointment',backref='pet',lazy='dynamic')

    def __repr__(self):
        return '<Pet {}>'.format(self.name)

class Appointment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.Integer,nullable=False)
    hospital_location = db.Column(db.Integer,nullable=False)
    time = db.Column(db.DateTime,index=True,default=datetime.now())
    status = db.Column(db.Integer,index=True,default=1)
    pet_status = db.Column(db.String(256),default='none')
    meeting_date = db.Column(db.DateTime,index=True,default=None)
    surgery_date = db.Column(db.DateTime,index=True,default=None )
    description = db.Column(db.String(256))
    pet_id = db.Column(db.Integer,db.ForeignKey('pet.id'))
    operator_id = db.Column(db.Integer,db.ForeignKey('staff.id'))

    def __repr__(self):
        return 'Appointment No.{}'.format(self.id)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True)
    content = db.Column(db.String(1500))
    time=db.Column(db.DateTime,index=True,default=datetime.now())
    answer =db.relationship('Answer', backref='question', lazy='dynamic')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __repr__(self):
        return '<Question:{}>'.format(self.title)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1500))
    time=db.Column(db.DateTime,index=True,default=datetime.now())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))

    def __repr__(self):
        return '<Answer:{}>'.format(self.body)