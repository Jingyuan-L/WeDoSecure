from db import db


class DriverModel(db.Model):
    __tablename__ = 'driver'

    driver_id = db.Column(db.Integer,primary_key=True)
    license_num = db.Column(db.String(12), nullable=False)
    driver_name = db.Column(db.String(30), nullable=False)
    driver_birthday = db.Column(db.Date, nullable=False)

    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, license_num, driver_name, driver_birthday, vehicle_id):
        self.license_num = license_num
        self.driver_name = driver_name
        self.driver_birthday = driver_birthday
        self.vehicle_id = vehicle_id

    def json(self):
        return {
            'driver_id': self.driver_id,
            'license_num': self.license_num,
            'driver_name': self.driver_name,
            'driver_birthday': self.driver_birthday,
            'vehicle_id': self.vehicle_id
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(driver_id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
