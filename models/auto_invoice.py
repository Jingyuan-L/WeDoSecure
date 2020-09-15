from db import db


class AutoInvoiceModel(db.Model):
    __tablename__ = 'auto_invoice'

    a_invoice_id = db.Column(db.Integer, primary_key=True)
    a_invoice_date = db.Column(db.Date, nullable=False)
    a_pay_due_date = db.Column(db.Date, nullable=False)
    a_invoice_amount = db.Column(db.DECIMAL(12, 2), nullable=False)

    customer_id = db.Column(db.Integer,
                            db.ForeignKey('auto_insurance.customer_id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, a_invoice_date, a_pay_due_date, a_invoice_amount, customer_id):
        self.a_invoice_date = a_invoice_date
        self.a_pay_due_date = a_pay_due_date
        self.a_invoice_amount = a_invoice_amount
        self.customer_id = customer_id

    def json(self):
        return {
            'a_invoice_id': self.a_invoice_id,
            'a_invoice_date': self.a_invoice_date,
            'a_pay_due_date': self.a_pay_due_date,
            'a_invoice_amount': self.a_invoice_amount,
            'customer_id': self.customer_id
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(a_invoice_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
