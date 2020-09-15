from flask_restful import Resource
from flask import request, redirect
from models.customer import CustomerModel


class CustomerInformation(Resource):
    # update data in database
    def post(self, customer_id):
        data = request.form
        print(data)
        new_cus = CustomerModel.query.get(customer_id)
        new_cus.password = data['password']
        new_cus.full_name = data['full_name']
        new_cus.address = data['address']
        new_cus.gender = data['gender']
        new_cus.marital_status = data['marital_status']
        new_cus.save_to_db()
        print("customer updated!")

        return redirect("/information/" + data['customer_id'])
