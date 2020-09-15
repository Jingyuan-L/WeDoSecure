from db import db


class HInsPaymentModel(db.Model):
    __tablename__ = 'h_ins_payment'

    h_payment_id = db.Column(db.Integer,primary_key=True)
    h_pay_amount = db.Column(db.DECIMAL(12,2), nullable=False)
    h_payment_date = db.Column(db.Date, nullable=False)
    h_payment_method = db.Column(db.Enum("Paypal", "Credit", "Debit", "Check"), nullable=False)

    h_invoice_id = db.Column(db.Integer, db.ForeignKey('home_invoice.h_invoice_id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, h_pay_amount,h_payment_date, h_payment_method, h_invoice_id):
        self.h_pay_amount = h_pay_amount
        self.h_payment_date = h_payment_date
        self.h_payment_method = h_payment_method
        self.h_invoice_id = h_invoice_id

    def json(self):
        return {
            'h_payment_id': self.h_payment_id,
            'h_pay_amount': self.h_pay_amount,
            'h_payment_date': self.h_payment_date,
            'h_payment_method': self.h_payment_method,
            'h_invoice_id': self.h_invoice_id
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(h_payment_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
