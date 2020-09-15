from db import db


class VehicleModel(db.Model):
    __tablename__ = 'vehicle'

    vehicle_id = db.Column(db.Integer,primary_key=True)
    vin = db.Column(db.String(12), nullable=False)
    model_year = db.Column(db.String(4), nullable=False)
    vehicle_status = db.Column(db.Enum("L", "F", "O"), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('auto_insurance.customer_id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, vin, model_year, vehicle_status, customer_id):
        self.vin = vin
        self.model_year = model_year
        self.vehicle_status = vehicle_status
        self.customer_id = customer_id

    def json(self):
        return {
            'vehicle_id': self.vehicle_id,
            'vin': self.vin,
            'model_year': self.model_year,
            'vehicle_status': self.vehicle_status,
            'custome_id': self.customer_id
        }

    @classmethod
    def find_by_vin(cls, vin):
        return cls.query.filter_by(vin=vin).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
