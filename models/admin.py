from urllib.parse import quote

from db import db


class AdminModel(db.Model):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def __init__(self, admin_name, password):
        self.admin_name = admin_name
        self.password = password

    def json(self):
        return {
            'id': self.admin_id,
            'username': self.admin_name
        }

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(admin_name=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(admin_id=_id).first()

    def save_to_db(self):
        password = self.password
        self.password = quote(password)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()