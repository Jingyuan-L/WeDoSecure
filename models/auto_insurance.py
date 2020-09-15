from db import db


class AutoInsuranceModel(db.Model):
    __tablename__ = 'auto_insurance'

    customer_id = db.Column(db.Integer,
                            db.ForeignKey('customer.customer_id', ondelete='CASCADE', onupdate='CASCADE'),
                            primary_key=True)
    a_start_date = db.Column(db.Date, nullable=False)
    a_end_date = db.Column(db.Date, nullable=False)
    a_premium_amount = db.Column(db.DECIMAL(12, 2), nullable=False)
    a_policy_status = db.Column(db.Enum("C", "P"))

    customer = db.relationship('CustomerModel')

    def __init__(self, customer_id, a_start_date, a_end_date, a_premium_amount, a_policy_status):
        self.customer_id = customer_id
        self.a_start_date = a_start_date
        self.a_end_date = a_end_date
        self.a_premium_amount = a_premium_amount
        self.a_policy_status = a_policy_status

    def json(self):
        return {
            'a_customer_id': self.a_customer_id,
            'a_start_data': self.a_start_date,
            'a_end_date': self.a_end_date,
            'a_premium_amount': self.a_premium_amount,
            'a_policy_status': self.a_policy_status
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
