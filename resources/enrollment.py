from datetime import datetime
from flask_restful import Resource
from flask import request, redirect
from models.auto_insurance import AutoInsuranceModel
from models.auto_invoice import AutoInvoiceModel
from models.driver import DriverModel
from models.home_insurance import HomeInsuranceModel
from models.home_invoice import HomeInvoiceModel
from models.home import HomeModel
from models.vehicle import VehicleModel
from models.customer import CustomerModel


class EnrollmentCustomer(Resource):
    def post(self):
        data = request.form
        print(data)
        if not CustomerModel.find_by_id(data['customer_id']):
            CustomerModel(data['customer_id'], data['password'], data['full_name'], data['address'],
                                     data['gender'], data['marital_status'], data['customer_type']).save_to_db()
            print("customer saved!")
            msg = "Customer enrolled successfully!"
            print(CustomerModel.query.filter(CustomerModel.customer_id == 10000001).first())
        else:
            msg = "Customer ID has exist!"

        def save_home():
            print("start saving home insurance")
            h_start_date = datetime.strptime(data['h_start_date'], "%Y-%m-%d").date()
            h_end_date = datetime.strptime(data['h_end_date'], "%Y-%m-%d").date()
            h_invoice_date = datetime.now()
            h_pay_due_date = datetime.strptime('2020-12-31', "%Y-%m-%d").date()
            purchase_date = datetime.strptime(data['purchase_date'], "%Y-%m-%d").date()
            print("date changed")
            HomeInsuranceModel(data['customer_id'], h_start_date, h_end_date,
                               data['h_premium_amount'], data['h_policy_status']).save_to_db()
            print("h ins saved")
            HomeInvoiceModel(h_invoice_date, h_pay_due_date,
                             data['h_premium_amount'], data['customer_id']).save_to_db()
            print("h inv saved")
            HomeModel(purchase_date, data['purchase_value'], data['area_sqft'], data['home_type'],
                      data['auto_fire_notif'], data['security_sys'], data['swimming_pool'], data['basement'],
                      data['customer_id']).save_to_db()
            print("home saved")

        def save_auto():
            print("start saving home insurance")
            a_start_date = datetime.strptime(data['a_start_date'], "%Y-%m-%d").date()
            a_end_date = datetime.strptime(data['a_end_date'], "%Y-%m-%d").date()
            a_invoice_date = datetime.now()
            a_pay_due_date = datetime.strptime('2020-12-31', "%Y-%m-%d").date()
            driver_birthday = datetime.strptime(data['driver_birthday'], "%Y-%m-%d").date()
            print("date changed")

            AutoInsuranceModel(data['customer_id'], a_start_date, a_end_date,
                               data['a_premium_amount'], data['a_policy_status']).save_to_db()
            print("a ins saved")
            AutoInvoiceModel(a_invoice_date, a_pay_due_date,
                             data['a_premium_amount'], data['customer_id']).save_to_db()
            print("a inv saved")
            VehicleModel(data['vin'], data['model_year'], data['vehicle_status'], data['customer_id']).save_to_db()
            print("vehicle saved")
            new_vehicle = VehicleModel.find_by_vin(data['vin'])
            DriverModel(data['license_num'], data['driver_name'], driver_birthday,
                        new_vehicle.vehicle_id).save_to_db()
            print("driver saved")

        if data['customer_type'] == "A":
            save_auto()
            print("auto insurance saved!")
        elif data['customer_type'] == "H":
            save_home()
            print("home insurance saved!")
        elif data['customer_type'] == "B":
            save_auto()
            save_home()
            print("both insurance saved!")

        return redirect("/information/"+data['customer_id'])
