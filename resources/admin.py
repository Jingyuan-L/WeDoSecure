from urllib.parse import quote
from flask_restful import Resource, request
from flask import redirect
from werkzeug.security import safe_str_cmp

from models.admin import AdminModel
from models.customer import CustomerModel


class Admin(Resource):
    def post(self):
        data = request.form
        admin = AdminModel.find_by_name(data['admin_name'])
        print(data)

        if admin and safe_str_cmp(admin.password, quote(data['password'])):
            return redirect("/admin_page")

        return {"message": "Invalid Admin!"}, 401


