from main import db

#Model

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column('User_id', db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))  
    contact_no = db.Column(db.Integer)
    sex = db.Column(db.String(6))