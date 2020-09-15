from hashlib import md5
from db import db


class CustomerModel(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(30), nullable=False)
    full_name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.Enum("M", "F"), nullable=False)
    marital_status = db.Column(db.Enum("S", "M", "W"), nullable=False)
    customer_type = db.Column(db.Enum("H", "A", "B"), nullable=False)

    def __init__(self, customer_id, password, full_name, address, gender, marital_status, customer_type):
        self.customer_id = customer_id
        self.full_name = full_name
        self.password = password
        self.address = address
        self.gender = gender
        self.marital_status = marital_status
        self.customer_type = customer_type

    def json(self):
        return {
            'customer_id': self.customer_id,
            'full_name': self.full_name,
            'password': self.password,
            'address': self.address,
            'gender': self.gender,
            'marital_status': self.marital_status,
            'customer_type': self.customer_type
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(full_name=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(customer_id=_id).first()

    def save_to_db(self):
        self.password = md5(self.password.encode("utf-8")).hexdigest()
        print(self.password)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
