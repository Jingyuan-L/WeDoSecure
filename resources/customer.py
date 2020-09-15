from hashlib import md5
from flask_restful import Resource
from flask import redirect, request
from werkzeug.security import safe_str_cmp

from models.customer import CustomerModel


class CustomerLogin(Resource):
    def post(self):
        data = request.form
        customer = CustomerModel.find_by_id(data['customer_id'])
        if customer and safe_str_cmp(customer.password, md5(data['password'].encode("utf-8")).hexdigest()):
            return redirect("/information/" + data['customer_id'])

        return {"message": "Invalid Credentials!"}, 401

