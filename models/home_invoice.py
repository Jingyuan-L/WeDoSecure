from db import db


class HomeInvoiceModel(db.Model):
    __tablename__ = 'home_invoice'

    h_invoice_id = db.Column(db.Integer, primary_key=True)
    h_invoice_date = db.Column(db.Date, nullable=False)
    h_pay_due_date = db.Column(db.Date, nullable=False)
    h_invoice_amount = db.Column(db.DECIMAL(12, 2), nullable=False)

    customer_id = db.Column(db.Integer,
                            db.ForeignKey('home_insurance.customer_id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, h_invoice_date, h_pay_due_date, h_invoice_amount, customer_id):
        self.h_invoice_date = h_invoice_date
        self.h_pay_due_date = h_pay_due_date
        self.h_invoice_amount = h_invoice_amount
        self.customer_id = customer_id

    def json(self):
        return {
            'h_invoice_id': self.h_invoice_id,
            'h_invoice_date': self.h_invoice_date,
            'h_pay_due_date': self.h_pay_due_date,
            'h_invoice_amount': self.h_invoice_amount,
            'customer_id': self.customer_id
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(h_invoice_id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
