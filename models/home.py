from db import db


class HomeModel(db.Model):
    __tablename__ = 'home'

    home_id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.Date, nullable=False)
    purchase_value = db.Column(db.DECIMAL(12), nullable=False)
    area_sqft = db.Column(db.Integer, nullable=False)
    home_type = db.Column(db.Enum("S", "M", "C", "T"), nullable=False)
    auto_fire_notif = db.Column(db.Enum("Y", "N"),nullable=False)
    security_sys = db.Column(db.Enum("Y", "N"), nullable=False)
    swimming_pool = db.Column(db.Enum("U", "O", "I", "M", "N"))
    basement = db.Column(db.Enum("Y", "N"), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('home_insurance.customer_id', onupdate='CASCADE', ondelete='CASCADE'))

    home_insurance = db.relationship('HomeInsuranceModel')

    def __init__(self, purchase_date, purchase_value, area_sqft, home_type, auto_fire_notif, security_sys, swimming_pool, basement, customer_id):
        self.purchase_date = purchase_date
        self.purchase_value = purchase_value
        self.area_sqft =area_sqft
        self.home_type = home_type
        self.auto_fire_notif = auto_fire_notif
        self.security_sys = security_sys
        self.swimming_pool = swimming_pool
        self.basement = basement
        self.customer_id = customer_id

    def json(self):
        return {
            'home_id': self.home_id,
            'purchase_date': self.purchase_date,
            'purchase_value': self.purchase_value,
            'area_sqft': self.area_sqft,
            'home_type': self.home_type,
            'auto_fire_notif': self.auto_fire_notif,
            'security_sys': self.security_sys,
            'swimming_pool': self.swimming_pool,
            'basement': self.basement,
            'customer_id': self.customer_id
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(home_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
