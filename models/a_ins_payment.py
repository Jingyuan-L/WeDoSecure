from db import db


class AInsPaymentModel(db.Model):
    __tablename__ = 'a_ins_payment'

    a_payment_id = db.Column(db.Integer, primary_key=True)
    a_pay_amount = db.Column(db.DECIMAL(12, 2), nullable=False)
    a_payment_date = db.Column(db.Date, nullable=False)
    a_payment_method = db.Column(db.Enum("Paypal", "Credit", "Debit", "Check"), nullable=False)

    a_invoice_id = db.Column(db.Integer, db.ForeignKey('auto_invoice.a_invoice_id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, a_pay_amount, a_payment_date, a_payment_method, a_invoice_id):
        self.a_pay_amount = a_pay_amount
        self.a_payment_date = a_payment_date
        self.a_payment_method = a_payment_method
        self.a_invoice_id = a_invoice_id

    def json(self):
        return {
            'a_payment_id': self.a_payment_id,
            'a_pay_amount': self.a_pay_amount,
            'a_payment_date': self.a_payment_date,
            'a_payment_method': self.a_payment_method,
            'a_invoice_id': self.a_invoice_id
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(a_payment_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
