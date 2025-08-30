
from amazon_app import db

class ProductItems(db.Model):
    print('creating a table')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    price = db.Column(db.Float, nullable=False)


class UsersTable(db.Model):
    print('creating users table')
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)



class OrdersTable(db.Model):
    print('creating orders table')
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)


class customersTable(db.Model):
    print('creating customers table')
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(50),unique=True,nullable=False)
    password=db.Column(db.String(50),nullable=False)

