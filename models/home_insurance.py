from db import db


class HomeInsuranceModel(db.Model):
    __tablename__ = 'home_insurance'

    customer_id = db.Column(db.Integer,
                            db.ForeignKey('customer.customer_id', ondelete='CASCADE', onupdate='CASCADE'),
                            primary_key=True)
    h_start_date = db.Column(db.Date, nullable=False)
    h_end_date = db.Column(db.Date, nullable=False)
    h_premium_amount = db.Column(db.DECIMAL(12, 2), nullable=False)
    h_policy_status = db.Column(db.Enum("C", "P"))

    customer = db.relationship('CustomerModel')

    def __init__(self, customer_id, start_date, end_date, premium_amount, policy_status):
        self.customer_id = customer_id
        self.h_start_date = start_date
        self.h_end_date = end_date
        self.h_premium_amount = premium_amount
        self.h_policy_status = policy_status

    def json(self):
        return {
            'h_customer_id': self.h_customer_id,
            'h_start_data': self.h_start_date,
            'h_end_date': self.h_end_date,
            'h_premium_amount': self.h_premium_amount,
            'h_policy_status': self.h_policy_status
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(customer_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()